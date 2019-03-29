# -*- coding:utf-8 -*-
import socket
from toolboxs import stoolbox as st
from toolboxs import ptoolbox as pt
import json
import traceback
import time
import threading


def sign_in(ckey):  # ok
    """
    认证接入是否合法

    参数
    1. ckey: 密钥

    返回值示例
    True
    """

    skey = "hack it and docker it!"
    return skey == ckey


def getImageList(mission):
    return {}


def recvd_msg(conn):  # ok
    """
    处理用户层发来的消息，根据任务的数据类型（dict 与 list）
    选择不同的处理方式与返回。
    具体任务由 stoolbox.py 中的函数完成

    参数
    1. conn: 建立起的通道

    {
        "mission": {
            "command": "getImageList",
            ...
        }
    }
    """

    results = json.dumps({
        "code": 1,
        "msg": "Message is empty",
        "result": ""
    })

    msg = conn.recv(1024)

    if not msg:  # 空消息，直接舍弃
        return

    try:
        mission = json.loads(msg)
    except Exception:  # json 格式有问题
        results['msg'] = 'JSON format is error'
    else:
        if 'mission' in mission and len(mission) == 1:
            command = list(mission)[0]

            func = funcs.get(command, None)
            if func:
                results['result'] = func(mission)
            else:  # 无此接口
                results['msg'] = 'Beyond my ability'
        else:
            results['msg'] = '''
Give me a json like:
{
    "mission": {
        "getImageList": "test"
    }
}
'''

    conn.sendall(results)


def multi_worker(conn):
    '''
    多线程进入到这函数，处理用户层发来的任务
    '''

    client_data = conn.recv(1024)

    if sign_in(client_data):
        conn.sendall('Go on')
        try:
            recvd_msg(conn)
        except Exception, e:
            print pt.put_color(u"处理信息时发生问题\n  [-]" + str(e), "red")
            print "-" * 50
            pt.log(
                traceback.format_exc(), level="error", description="slave(%s) recvd mission but can't finish it" %
                st.setting["bridge"]["self_ip"], path=".slave_log"
            )

            conn.sendall(json.dumps([{
                "code": 1,
                "msg": str(e),
                "result": "",
            }]))
    else:
        msg = u"来自 %s:%s 的非法访问. Silence is gold" % from_ip
        print pt.put_color(msg, "yellow")
        conn.sendall('Silence is gold...')

    conn.close()


"""
监听端口，负责建立通信

1. ip: 允许接入的 ip；默认为 0.0.0.0, 即任意 ip
2. port: 监听的端口; 可选参数; 默认为 1122
"""

funcs = {
    'getImageList': getImageList,
}


ip = '0.0.0.0'
port = 1111
sk = socket.socket()
sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sk.bind((ip, port))
sk.listen(100)

print pt.put_color('server is online', "green")

while 1:
    try:
        conn, from_ip = sk.accept()
        th = threading.Thread(target=multi_worker, args=(conn,))
        th.start()
    except KeyboardInterrupt:
        break
    except Exception, e:
        print pt.put_color(u"出现一个隐藏问题\n  [-]" + str(e), "red")
        print "-" * 50
        pt.log(
            traceback.format_exc(), level="error",
            description="server reported an error", path=".slave_log"
        )

        break

print pt.put_color('server is offline', "red")
