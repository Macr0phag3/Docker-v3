# -*- coding: utf-8 -*-


class API:
    # 新增的 api 放在这

    # !!! api 约定 !!!
    '''
    - api 命名：api_xxxx

    - mission 格式为：
    {
        "mission": {
            "getImageList": ["test"]
        }
    }

    - api 必须返回 json

    '''

    def api_getImageList(mission):
        return '{}'

    def api_pullImage():
        return '{}'


apis = {i[4:]: getattr(API, i) for i in dir(API) if i[:4] == 'api_'}
