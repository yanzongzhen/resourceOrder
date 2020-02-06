# _*_coding:utf-8_*_
"""
@ProjectName: resourceOrder
@Author:  Javen Yan
@File: libs.py
@Software: PyCharm
@Time :    2020/2/6 下午12:47
"""

from web.models.databases import Areas, SyStoreModel
from web.utils.date2json import to_json
from web.apps.base.status import StatusCode


async def get_area(self, parent_code, region_code):
    results = []
    rows = Areas.filter(parent_code, region_code)
    if rows:
        results = to_json(rows)
    return {'status': True, 'msg': "获取成功", "data": results, "code": StatusCode.success.value}


async def get_hospital(self, district, latitude, longitude, limit):
    result = None
    if not latitude and not longitude:
        rows = SyStoreModel.by_address(district, limit)
        if rows:
            result = to_json(rows)
    elif district:
        if latitude and longitude:
            rows = SyStoreModel.filter(district, latitude, longitude, limit)
            if rows:
                result = rows
        else:
            rows = SyStoreModel.by_address(district, limit)
            if rows:
                result = to_json(rows)
    return {'status': True, 'msg': "获取成功", "data": result, "code": StatusCode.success.value}