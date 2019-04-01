# -*- coding:utf-8 -*-
import socket
import json
import traceback
import time
import threading

import toolbox
import apis


class Worker:
    '''
    Master 派任务给 Worker
    直接向后端返回 api 所需的数据
    '''

    def __init__(self, conn):
        self.conn = conn  # socket 通道
        self.api_list = {
            i[4:]: getattr(apis, i)
            for i in dir(apis) if i[:4] == 'api_'
        }

    def _api(self):  # ok
        """
        处理 api 调用
        具体任务由 stoolbox.py 中的函数完成

        {
            "mission": {
                "command": "getImageList",
                ...
            }
        }
        """

        results = {
            "code": 1,
            "msg": "",
            "result": ""
        }

        msg = self.conn.recv(1024)

        if not msg:  # 空消息，直接舍弃
            return

        try:
            mission = json.loads(msg)
        except Exception:  # json 格式有问题
            results['msg'] = 'The json has syntax error'
        else:  # json 不为空
            if len(mission) == 1 and type(mission[list(mission)[0]]) == list:
                api = list(mission)[0]  # 获取调用的 api 名
                func = self.api_list.get(api, None)
                if func:  # api 存在
                    results['code'] = 0
                    results['result'] = func(mission, *mission[api])
                else:
                    results['msg'] = 'This api was gone with wind'
            else:
                results['msg'] = '''
Give me a json like:
{
    "api_name": ["arg1", "arg2"]
}'''

        self.conn.sendall(json.dumps(results))

    def working(self):
        '''
        多线程处理 api 调用
        具体的事情留给 _api() 处理，这里只处理异常
        '''

        try:
            self._api()
        except Exception, e:
            print toolbox.put_color(u"调用 _api() 时出现问题\n  [-]" + str(e), "red")
            print "-" * 50
            toolbox.log(
                traceback.format_exc(),
                level="error", description="Something went wrong in _api()",
                path=".master_log"
            )

            self.conn.sendall(json.dumps([{
                "code": 1,
                "msg": 'Something went wrong',
                "result": "",
            }]))

        self.conn.close()


class Master:
    """
    Master 负责接受后端的 api 调用，
    并多线程启动 Worker
    """

    def __init__(self, ip, port, api_key='hack it and docker it!'):
        '''
        1. ip: 允许接入的 ip；默认为 0.0.0.0, 即任意 ip
        2. port: 监听的端口; 可选参数; 默认为 1122
        3. api_key: 调用 api 的认证手段
        '''
        self.ip = ip
        self.port = port
        self.api_key = api_key

    def listening(self):
        sk = socket.socket()

        # 防止 ctrl+c 后占用端口
        sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sk.bind((ip, port))
        sk.listen(1)

        print toolbox.put_color('Master is online', "green")
        while 1:
            try:
                conn, from_ip = sk.accept()
                api_key = conn.recv(1024)
                if api_key == self.api_key:  # 通过认证
                    conn.sendall('Go on')
                    worker = Worker(conn)
                    th = threading.Thread(target=worker.working)
                    th.start()
                else:
                    msg = u"来自 %s:%s 的非法访问. Silence is gold" % from_ip
                    print toolbox.put_color(msg, "yellow")
                    conn.sendall('Silence is gold...')
            except KeyboardInterrupt:
                print toolbox.put_color('Master is offline', "red")
                break
            except Exception, e:
                print toolbox.put_color(u"出现一个隐藏问题\n  [-]" + str(e), "red")
                print "-" * 50
                toolbox.log(
                    traceback.format_exc(), level="error",
                    description="Master reported an error",
                    path=".master_log"
                )
                break


ip = '0.0.0.0'
port = 1111

master = Master(ip, port)
master.listening()
