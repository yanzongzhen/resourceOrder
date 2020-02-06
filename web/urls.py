# _*_coding:utf-8_*_
"""
@ProjectName: Anti2019-nCoV
@Author:  Javen Yan
@File: urls.py
@Software: PyCharm
@Time :    2019/12/5 上午10:41
"""
from web.utils.app_route import merge_route
from web.apps.region.urls import urlpatterns as region
from web.apps.orders.urls import urlpatterns as orders
from web.apps.product.urls import urlpatterns as products
from web.apps.sms.urls import urlpatterns as sms


urlpatterns = list()


urlpatterns += merge_route(region, '/address')
urlpatterns += merge_route(orders, '/orders')
urlpatterns += merge_route(products, '/items')
urlpatterns += merge_route(sms, '/sms')