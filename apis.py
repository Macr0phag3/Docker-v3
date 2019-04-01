# -*- coding: utf-8 -*-

import toolbox

# 新增的 api 放在这

# !!! api 约定 !!!
'''
- api 函数命名：api_xxxx

- api 函数必须返回 json，示例:
dicts = {
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

    return toolbox.send_mission('192.168.12.1', mission)


