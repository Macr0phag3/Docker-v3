# -*- coding: utf-8 -*-

import toolbox
import json
import traceback
import docker
import commands

# 新增的 api 放在这

# !!! api 约定 !!!
'''
- api 函数命名：api_xxxx

- api 函数必须返回字典，示例:
results = {
    "code": 0,
    "msg": "",
    "result": "" # 与 slave 返回的值一致
}
'''

# ------------- 镜像相关 -------------


def api_getImagesList():
    """
    所有镜像的列表

    返回值示例
    dicts = {
        "code": 1,
        "msg": "",
        "result": [
            "image_name_1",
            "image_name_2"
        ]
    }
    """
    results = {
        "code": 0,
        "msg": "",
        "result": []
    }

    try:
        results["result"] = json.loads(commands.getoutput(
            'curl -s 127.0.0.1:5000/v2/_catalog'))['repositories']
    except Exception, e:
        toolbox.log(traceback.format_exc(), level="error",
                    description="get all images failed", path=".slave_log")

        results["code"] = 1
        results["msg"] = "master(%s) report a error: %s" % (
            setting["bridge"]["self_ip"], str(e))

    return results


def api_pullImages(image_names):
    '''
    拉取镜像
    1. image_names: 镜像名，列表
    '''
    mission = {
        "mission": "cmd2slave",  # 具体的任务
        "commands": {
            "command": "pull_images",  # 具体的命令
            "arg": [image_names],  # 参数列表
        }
    }

    results = {
        "code": 0,
        "msg": "",
        "result": {
            i: {
                'code': 0,
                'msg': '',
                'result': ''
            } for i in setting["slave_ip"]
        }
    }

    for ip in ['192.168.12.1']:  # setting["slave_ip"]:
        result = json.loads(toolbox.send_mission(ip, mission))
        if result["code"]:
            results['result'][ip]['code'] = 1
            results['result'][ip]['msg'] = result['msg']
        else:
            results['result'][ip]['result'] = result['result']

    return results


def api_deleteImages():
    return '{}'

# ------------- 容器相关 -------------


def api_getContainersList():
    '''
    所有容器的列表
    '''
    mission = {
        "mission": "cmd2docker",  # 具体的任务
        "commands": {
            "command": "containers_ls",  # 具体的命令
            "arg": [],  # 参数列表
        }
    }

    results = {
        "code": 0,
        "msg": "",
        "result": {
            i: {
                'code': 0,
                'msg': '',
                'result': []
            } for i in setting["slave_ip"]
        }
    }

    for ip in setting["slave_ip"]:
        result = json.loads(toolbox.send_mission(ip, mission))
        if result["code"]:
            results['result'][ip]['code'] = 1
            results['result'][ip]['msg'] = result['msg']
        else:
            results['result'][ip]['result'] = result['result']

    return results



# ------------- 载入配置 -------------
try:
    with open(".setting", "r") as fp:
        setting = json.load(fp)
except Exception, e:
    print toolbox.put_color(u"载入配置出错", "red")
    print str(e)
    toolbox.log(traceback.format_exc(), level="error",
                description="load setting failed!", path=".slave_log")
    raise
