# -*- coding:utf-8 -*-
import time
import socket

def log(msg, level, description, path):  # ok
    """
    记录事件，默认路径为 slave.py 所在路径
    log 文件名为 .slave_log

    参数:
    1. level: 事件等级
    2. description: 事件描述
    3. message: 事件原因的具体描述
    4. path: log 文件的路径(包括文件名)
    """

    with open(path, "a") as fp:
        fp.write(
            "[%s]\nlevel: %s\ndescription: %s\nmessage: %s\n\n" % (
                time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime()
                ),
                level, description.encode("utf8"), msg)
        )


def put_color(string, color):  # ok
    colors = {
        "red": "31",
        "green": "32",
        "yellow": "33",
        "blue": "34",
        "pink": "35",
        "cyan": "36",
        "white": "37",
    }
    return "\033[40;1;%s;40m%s\033[0m" % (colors[color], string)



def send_mission(ip, mission, port=1122, timeout=60):  # ok
    """
    对 slave 指派任务

    参数
    1. ip: slave 的 ip
    2. mission，字典: 具体任务, 格式如下：
        {
            "mission": "", # 具体的任务
            "commands":
            {
                "command": "", # 具体的命令
                "arg": [],  # 参数列表
            }
        }
    3. port: 与 slave 的通信端口; 可选; 默认为 1122
    4. timeout: 等待 slave 返回的超时时间; 可选; 默认为 60s

    返回值示例
    dicts = {
        "code": 0,
        "msg": "",
        "result": "" # 与 slave 返回的值一致
    }
    """

    dicts = {
        "code": 1,
        "msg": "",
        "result": ""
    }

    socket.setdefaulttimeout(timeout)
    sk = socket.socket()
    for i in range(3): # 尝试 3 次连接
        try:
            sk.connect((ip, port))
            break
        except Exception, e:
            if i == 2:
                log(traceback.format_exc(), level="error",
                       description="connect to slave: %s:%s failed" % (ip, port), path=".master_log")

                dicts["msg"] = "connect to slave: %s:%s failed" % (ip, port)
                return json.dumps(dicts)

    try:
        sk.sendall("hack it and docker it!")  # 认证 key
        server_reply = sk.recv(1024)

        if server_reply == "hello, my master":  # 认证成功
            sk.sendall(json.dumps(mission))
            dicts = json.loads(sk.recv(1024000))
            sk.close()
        else:  # 认证失败
            dicts["msg"] = "sign in failed"

    except Exception, e:
        log(
            traceback.format_exc(), level="error",
               description="send a mission to slave(%s) failed" % (ip), path=".master_log")

        dicts["msg"] = "send a mission to slave(%s) failed: %s" % (ip, str(e))

    return json.dumps(dicts)



