# _*_coding:utf-8_*_
"""
@ProjectName: resourceOrder
@Author:  Javen Yan
@File: urls.py
@Software: PyCharm
@Time :    2020/2/6 下午7:32
"""

from web.apps.admin.controller import AdminUserLoginHandler, AdminUserRegisterHandler, AdminUserProfile
from web.apps.product.controller import ProductsHandler
from web.apps.orders.controller import OrderVerifyHandler, OrderUserHandler

urlpatterns = [
    (r'/login', AdminUserLoginHandler),
    (r'/register', AdminUserRegisterHandler),
    (r'/profile', AdminUserProfile),
    (r'/items', ProductsHandler),
    (r'/orders/verify', OrderVerifyHandler),
    (r'/orders/user', OrderUserHandler)
]