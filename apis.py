# -*- coding: utf-8 -*-

# 新增的 api 放在这

# !!! api 约定 !!!
'''
- api 函数命名：api_xxxx
- api 函数至少有一个参数，叫 mission
- mission 格式为：
{
    "mission": {
        "getImageList": ["test"]
    }
}

- api 函数必须返回 json

'''

# ------------- 镜像相关 -------------


def api_getImageList(mission):
    return '{}'


def api_pullImage(mission):
    return '{}'


def api_deleteImage(mission):
    return '{}'

# ------------- 容器相关 -------------


def api_getContainerList(mission):
    return '{}'



















