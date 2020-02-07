# _*_coding:utf-8_*_
"""
@ProjectName: resourceOrder
@Author:  Javen Yan
@File: libs.py
@Software: PyCharm
@Time :    2020/2/6 下午4:58
"""
import json
import time
from random import randint
import httpx as requests
from logzero import logger
from web.apps.base.status import StatusCode
from web.models.databases import SMSRecord


async def send_sms(self, phone):

    url = "https://new.icity24.cn/gateway/api-sms/verification/sendOneMessage"
    code = str(randint(100000, 999999))
    data = {
        "params": json.dumps({
            "mobile": phone,
            "messageContent": f"【爱城市网】您本次登录的验证码为：{code}，验证码30分钟内有效"
        })
    }
    try:
        response = await requests.post(url, data=data)
        if 300 > response.status_code >= 200:
            content = response.json()
            if content.get('code') == '0000':
                sms = SMSRecord(phone=phone, code=code, createdTime=int(time.time()))
                self.db.add(sms)
                self.db.commit()
                return {"status": True, "code": StatusCode.success.value, "msg": "短信发送成功"}
            else:
                return {"status": False, "code": StatusCode.error.value,"msg": "短信发送失败"}
    except Exception as e:
        logger.error(f"Send Msg error {e}")
        return {"status": False, "code": StatusCode.error.value,"msg": "短信发送失败"}
