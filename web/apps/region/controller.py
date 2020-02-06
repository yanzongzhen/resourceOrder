# _*_coding:utf-8_*_
"""
@ProjectName: resourceOrder
@Author:  Javen Yan
@File: controller.py
@Software: PyCharm
@Time :    2020/2/6 下午12:45
"""
from web.apps.base.controller import BaseRequestHandler,ABC
from web.apps.region.libs import get_area, get_hospital


class RegionHandler(BaseRequestHandler,ABC):

    async def get(self):
        response = dict()
        parent_code = self.get_argument('parent', None)
        region_code = self.get_argument('regionCode', None)
        result = await get_area(self, parent_code, region_code)
        response['code'] = result['code']
        response['message'] = result['msg']
        if result['status']:
            response['data'] = result['data']
        return self.write_json(response)


class HospitalHandler(BaseRequestHandler, ABC):

    async def get(self):
        response = dict()
        district = self.get_argument('district', None)
        latitude = self.get_argument('latitude', None)
        longitude = self.get_argument('longitude', None)
        limit = int(self.get_argument('limit', '10'))
        result = await get_hospital(self, district, latitude, longitude, limit)
        response['code'] = result['code']
        response['message'] = result['msg']
        if result['status']:
            response['data'] = result['data']
        return self.write_json(response)