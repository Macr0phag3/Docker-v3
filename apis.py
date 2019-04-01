# -*- coding: utf-8 -*-

import toolbox

# 新增的 api 放在这

# !!! api 约定 !!!
'''
- api 函数命名：api_xxxx

- api 函数必须返回 json，示例:
results = {
    "code": 0,
    "msg": "",
    "result": "" # 与 slave 返回的值一致
}
'''

# ------------- 镜像相关 -------------


def api_getImageList():
    return '{}'


def api_pullImage():
    return '{}'


def api_deleteImage():
    return '{}'

# ------------- 容器相关 -------------


def api_getContainerList():
    mission = {
        "mission": "cmd2docker",  # 具体的任务
        "commands":
            {
                "command": "containers_ls",  # 具体的命令
                "arg": [],  # 参数列表
            }
    }

    results = {
        "code": 1,
        "msg": "",
        "result": {
            i: {
                'code': 1,
                'msg': '',
                'result': []
            } for i in setting["slave_ip"]
        }
    }

    for ip in setting["slave_ip"]:
        result = json.loads(toolbox.send_mission(ip, mission))
        if result["code"]:
            results['result']['ip']['msg'] = result['msg']
        else:
            results['result']['ip']['code'] = 0
            results['result']['ip']['result'] = result['result']

    return results


# ------------- 载入配置 -------------
try:
    with open(".setting", "r") as fp:
        setting = json.load(fp)
except Exception, e:
    print pt.put_color(u"载入配置出错", "red")
    print str(e)
    pt.log(traceback.format_exc(), level="error",
           description="load setting failed!", path=".slave_log")
    raise
