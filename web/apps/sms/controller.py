# _*_coding:utf-8_*_
"""
@ProjectName: resourceOrder
@Author:  Javen Yan
@File: controller.py
@Software: PyCharm
@Time :    2020/2/6 下午4:54
"""
from web.apps.base.controller import BaseRequestHandler,ABC
from web.apps.sms.libs import send_sms


class SmsHandler(BaseRequestHandler,ABC):

    async def get(self):
        response = dict()
        mobile = self.get_argument('mobile', None)
        if not mobile:
            response['code'] = 10001
            response['message'] = "缺少参数"
        else:
            result = await send_sms(self, mobile)
            response['code'] = result['code']
            response['message'] = result['msg']
        return self.write_json(response)
