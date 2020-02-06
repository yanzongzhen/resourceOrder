# _*_coding:utf-8_*_
"""
@ProjectName: resourceOrder
@Author:  Javen Yan
@File: urls.py
@Software: PyCharm
@Time :    2020/2/6 下午4:54
"""

from web.apps.sms.controller import SmsHandler


urlpatterns = [
    (r'/sender', SmsHandler)
]