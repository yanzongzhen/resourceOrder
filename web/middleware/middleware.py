# _*_coding:utf-8_*_
"""
@ProjectName: Anti2019-nCoV
@Author:  Javen Yan
@File: middleware.py
@Software: PyCharm
@Time :    2019/12/9 上午9:50
"""

from logzero import logger
from web.middleware.base import Middleware
from web.models.databases import AdminUser
from web.apps.base.status import StatusCode


class UserAuthMiddleware(Middleware):
    """
        微信用户认证中间件
    """

    async def process_request(self):
        logger.debug("用户认证中间件， 正在认证")
        openid = self.request.headers.get('openid', None)
        if openid is None:
            kw = {"code": StatusCode.no_auth_error.value, "message": "用户认证数据缺失"}
            return self.finish(kw)
        self.openid = openid    # 传入openid
        self.current_user = await get_user(self, openid)

    def process_response(self):
        logger.debug("用户认证中间件， 认证完成")


async def get_user(self, openid):
    return AdminUser.by_openid(openid)


class AdminMiddleware(Middleware):
    """
        微信用户认证中间件
    """

    async def process_request(self):
        if self.current_user and not self.current_user.is_admin:
            kw = {"code": StatusCode.no_access_error.value, "message": "您无权操作此业务"}
            return self.finish(kw)

    def process_response(self):
        logger.debug("ADMIN认证中间件， 认证完成")
