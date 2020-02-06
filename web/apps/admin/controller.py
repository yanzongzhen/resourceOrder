# _*_coding:utf-8_*_
"""
@ProjectName: resourceOrder
@Author:  Javen Yan
@File: controller.py
@Software: PyCharm
@Time :    2020/2/6 下午7:32
"""
from web.apps.base.controller import BaseRequestHandler, ABC, AuthRequestHandler
from web.apps.admin.libs import register, login, updateUser


class AdminUserLoginHandler(BaseRequestHandler, ABC):

    async def post(self):
        response = dict()
        payloads = self.get_payload()
        result = await login(self, payloads)
        response['code'] = result['code']
        response['message'] = result['msg']
        if result['status']:
            response['data'] = result['data']
        return self.write_json(response)


class AdminUserRegisterHandler(BaseRequestHandler, ABC):

    async def post(self):
        response = dict()
        payloads = self.get_payload()
        result = await register(self, payloads)
        response['code'] = result['code']
        response['message'] = result['msg']
        if result['status']:
            response['data'] = result['data']
        return self.write_json(response)


class AdminUserProfile(AuthRequestHandler, ABC):

    def get(self):
        response = dict()
        response['code'] = 10000
        response['message'] = "获取成功"
        response['data'] = self.current_user.to_dict()
        return self.write_json(response)

    async def post(self):
        response = dict()
        payloads = self.get_payload()
        result = await updateUser(self, payloads)
        response['code'] = result['code']
        response['message'] = result['msg']
        if result['status']:
            response['data'] = result['data']
        return self.write_json(response)