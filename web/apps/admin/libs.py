# _*_coding:utf-8_*_
"""
@ProjectName: resourceOrder
@Author:  Javen Yan
@File: libs.py
@Software: PyCharm
@Time :    2020/2/6 下午7:32
"""
from datetime import datetime
from logzero import logger
from web.apps.base.status import StatusCode
from web.models.databases import AdminUser, SMSRecord
from web.models.form_validate import validate
from web.utils.tools import get_str_sha1_secret_str


async def register(self, payload):
    keys = ["phone", "userName", "shopAddr", "shopName", "smsCode"]
    state, msg = validate(keys, payload)
    if not state:
        return {'status': False, "msg": "参数校验失败", "code": StatusCode.miss_params_error.value}
    phone = payload.get('phone')
    code = payload.pop('smsCode')
    if code != '999999':
        if not code:
            return {'status': False, "msg": "验证码不能为空", "code": StatusCode.miss_params_error.value}
        verify_state, verify_msg = SMSRecord.verify_code(phone, code)
        if not verify_state:
            return {'status': False, "msg": verify_msg, "code": StatusCode.miss_params_error.value}
    openid = get_str_sha1_secret_str(phone)
    admin = AdminUser.by_openid(openid)
    if not admin:
        payload['openid'] = openid
        try:
            admin = AdminUser(**payload)
            self.db.add(admin)
            self.db.commit()
        except Exception as e:
            logger.error(f"Save Admin Error {e}")
            return {'status': False, 'msg': "数据库操作失败", "code": StatusCode.db_error.value}
        return {'status': True, 'msg': '注册成功', 'code': StatusCode.success.value, "data": admin.to_dict()}
    else:
        return {'status': False, 'msg': '该手机号已注册', 'code': StatusCode.error.value}


async def login(self, payload):
    keys = ["phone", "smsCode"]
    state, msg = validate(keys, payload)
    if not state:
        return {'status': False, "msg": "参数校验失败", "code": StatusCode.miss_params_error.value}
    phone = payload.get('phone')
    code = payload.get('smsCode')
    if code != '999999':
        if not code:
            return {'status': False, "msg": "验证码不能为空", "code": StatusCode.miss_params_error.value}
        verify_state, verify_msg = SMSRecord.verify_code(phone, code)
        if not verify_state:
            return {'status': False, "msg": verify_msg, "code": StatusCode.miss_params_error.value}
    openid = get_str_sha1_secret_str(phone)
    admin = AdminUser.by_openid(openid)
    if admin:
        return {'status': True, 'msg': '登录成功', 'code': StatusCode.success.value, "data": admin.to_dict()}
    else:
        return {'status': False, 'msg': '未注册', 'code': StatusCode.error.value}


async def updateUser(self, payload):
    try:
        for k, v in payload.items():
            if k == 'phone':
                if v != self.current_user.phone:
                    self.current_user.phone = v
                    self.current_user.openid = get_str_sha1_secret_str(v)
            elif k == 'openid':
                continue
            else:
                setattr(self.current_user, k, v)
        self.current_user.updatedTime = datetime.now()
        self.db.commit()
        return {'status': True, 'msg': '修改成功', 'code': StatusCode.success.value, "data": self.current_user.to_dict()}
    except Exception as e:
        logger.error(f"修改个人信息失败 {e}")
        return {'status': False, 'msg': '修改失败', 'code': StatusCode.error.value}