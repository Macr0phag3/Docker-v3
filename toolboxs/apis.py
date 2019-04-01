# -*- coding: utf-8 -*-


def _getImageList(mission, *arg):
    print(arg)
    return '{}'


# 新增的 api 放在这
# api 约定：
'''
- mission 格式为：
{
    "mission": {
        "getImageList": ["test"]
    }
}

- 必须返回 json

'''
apis = {
    'getImageList': _getImageList,
}
