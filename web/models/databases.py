# _*_coding:utf-8_*_
"""
@ProjectName: Anti2019-nCoV
@Author:  Javen Yan
@File: databases.py
@Software: PyCharm
@Time :    2019/12/5 上午10:48
"""
from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, Integer, String, TEXT, DateTime, and_, Boolean, Float, text
from web.models.dbSession import ModelBase, dbSession
from web.utils.date2json import to_json
import time


def format_time(_time):
    """格式化时间"""
    return _time.strftime('%Y-%m-%d %H:%M:%S') if _time else ''


class AdminUser(ModelBase):
    __tablename__ = 'admin_user'

    id = Column(Integer, autoincrement=True, primary_key=True)
    userName = Column(String(32), comment="姓名")
    phone = Column(String(32), comment="手机")
    openid = Column(String(255), unique=True, comment="唯一登录id")
    shopAddr = Column(String(255), comment="药店地址")
    shopName = Column(String(128), comment="药店")
    is_admin = Column(Boolean, default=False, comment="1 管理员 0 店长")
    createTime = Column(DateTime, default=datetime.now, comment="创建时间")
    updateTime = Column(DateTime, nullable=True, comment="更新时间")

    @classmethod
    def by_openid(cls, kid):
        return dbSession.query(cls).filter_by(openid=kid).first()

    def to_dict(self):
        return {
            "userName": self.userName,
            "phone": self.phone,
            "openid": self.openid,
            "shopAddr": self.shopAddr,
            "shopName": self.shopName,
            "createTime": format_time(self.createTime),
            "updateTime": format_time(self.updateTime)
        }


class OrderUser(ModelBase):
    __tablename__ = 'order_user'

    id = Column(Integer, autoincrement=True, primary_key=True)
    userName = Column(String(32), comment="姓名")
    userPhone = Column(String(32), comment="手机")
    userIdCard = Column(String(64), comment="身份证")
    communityName = Column(TEXT, comment="社区名称")
    communityDistrict = Column(String(64), comment="社区地区")
    communityAddress = Column(TEXT, comment="社区地址")
    createTime = Column(DateTime, default=datetime.now(), comment="创建时间")
    updateTime = Column(DateTime, nullable=True, comment="更新时间")

    @classmethod
    def by_id(cls, kid):
        return dbSession.query(cls).filter_by(id=kid).first()

    @classmethod
    def by_id_card(cls, id_card):
        return dbSession.query(cls).filter_by(userIdCard=id_card).first()

    @classmethod
    def by_phone(cls, userPhone):
        return dbSession.query(cls).filter_by(userPhone=userPhone).first()

    @classmethod
    def all(cls):
        return dbSession.query(cls).all()

    @property
    def orders(self):
        rows = Orders.by_user_id(self.id)
        return to_json(rows) if rows else None

    @classmethod
    def filter(cls, id_card, phone):
        if id_card and not phone:
            return cls.by_id_card(id_card), 'dict'
        elif not id_card and phone:
            return cls.by_phone(phone), 'dict'
        else:
            return cls.all(), 'list'

    @classmethod
    def paginate(cls, page=1, page_size=10):
        start = page_size * (page - 1)
        end = page * page_size
        return dbSession.query(cls).slice(start, end).all()

    @classmethod
    def add(cls, **kwargs):
        """增加一行数据"""
        new_row = OrderUser(**kwargs)
        dbSession.add(new_row)
        dbSession.commit()
        return new_row

    def update(self, **kwargs):
        """根据实例更新数据"""
        kwargs['updateTime'] = datetime.now()
        row = dbSession.query(OrderUser).filter_by(id=self.id).first()
        for k, v in kwargs.items():
            setattr(row, k, v)
        dbSession.commit()
        return row

    def delete(self):
        """删除一个实例"""
        dbSession.query(OrderUser).filter_by(id=self.id).delete()
        dbSession.commit()

    def to_dict(self):
        return {
            "userName": self.userName,
            "userPhone": self.userPhone,
            "userIdCard": self.userIdCard,
            'community': {
                "name": self.communityName,
                "district": self.communityDistrict,
                "address": self.communityAddress
            },
            'orders': self.orders,
            "createTime": format_time(self.createTime),
            "updateTime": format_time(self.updateTime)
        }


class Areas(ModelBase):
    __tablename__ = 'areas'

    id = Column(Integer, autoincrement=True, primary_key=True)
    RegionCode = Column(String(32), comment="地区代码")
    RegionName = Column(String(128), comment="地区名称")
    Parent = Column(String(32), comment="父地址")

    @classmethod
    def by_region_code(cls, code):
        return dbSession.query(cls).filter(cls.RegionCode == code).all()

    @classmethod
    def by_parent_code(cls, code):
        return dbSession.query(cls).filter(cls.Parent == code).all()

    @classmethod
    def by_parent_and_region(cls, p_code, r_code):
        return dbSession.query(cls).filter(and_(cls.Parent == p_code, cls.RegionCode == r_code)).all()

    @classmethod
    def filter(cls, parent_code, region_code):
        if parent_code and not region_code:
            return cls.by_parent_code(parent_code)
        elif not parent_code and region_code:
            return cls.by_region_code(region_code)
        elif region_code and parent_code:
            return cls.by_parent_and_region(parent_code, region_code)
        else:
            return cls.all()

    @classmethod
    def all(cls):
        return dbSession.query(cls).all()

    @classmethod
    def add(cls, **kwargs):
        """增加一行数据"""
        new_row = Areas(**kwargs)
        dbSession.add(new_row)
        dbSession.commit()
        return new_row

    def to_dict(self):
        return {
            "RegionCode": self.RegionCode,
            "RegionName": self.RegionName,
            "Parent": self.Parent
        }


class Orders(ModelBase):
    __tablename__ = 'orders'

    COMMIT = 0
    SUCCESS = 1

    id = Column(Integer, autoincrement=True, primary_key=True)
    uuid = Column(String(64), default=lambda: str(uuid4()), comment="订单唯一标识码")
    userId = Column(Integer, comment="用户id")
    productName = Column(String(255), comment="商品名词")
    productQty = Column(Integer, comment="商品个数")
    pharmacyName = Column(TEXT, comment="药店名称")
    pharmacyDistrict = Column(String(64), comment="药店地区")
    pharmacyAddress = Column(TEXT, comment="药店地址")
    Status = Column(Integer, default=COMMIT, comment="是否完成 0 创建  1 完成")
    createdTime = Column(DateTime, default=datetime.now, comment="提交时间")
    updatedTime = Column(DateTime, comment="更新时间")

    @classmethod
    def all(cls):
        return dbSession.query(cls).order_by(-cls.createdTime).all()

    @classmethod
    def by_uuid(cls, uuid):
        return dbSession.query(cls).filter(cls.uuid == uuid).first()

    @classmethod
    def paginate(cls, page=1, page_size=10):
        start = page_size * (page - 1)
        end = page * page_size
        return dbSession.query(cls).order_by(-cls.createdTime).slice(start, end).all()

    @classmethod
    def by_user_id(cls, user_id):
        return dbSession.query(cls).order_by(-cls.createdTime).filter(cls.userId == user_id).all()

    @classmethod
    def order_over(cls, uuid):
        order = dbSession.query(cls).filter(cls.uuid == uuid).first()
        if order:
            order.Status = Orders.SUCCESS
            order.updatedTime = datetime.now()
            dbSession.commit()

    def update(self, **kwargs):
        """根据实例更新数据"""
        kwargs['updateTime'] = datetime.now()
        row = dbSession.query(Orders).filter_by(uuid=self.uuid).first()
        for k, v in kwargs.items():
            setattr(row, k, v)
        dbSession.commit()
        return row

    @property
    def inQueue(self):
        return len(dbSession.query(Orders).filter(and_(Orders.id < self.id, Orders.Status == Orders.COMMIT)).all())

    def to_dict(self):
        return {
            "uuid": self.uuid,
            "inQueue": self.inQueue,
            "status": self.Status,
            "pharmacy": {
                "name": self.pharmacyName,
                "district": self.pharmacyDistrict,
                "address": self.pharmacyAddress
            },
            "item": {
                "name": self.productName,
                "quantity": self.productQty
            },
            "createdTime": format_time(self.createdTime),
            "updatedTime": format_time(self.updatedTime)
        }


class Products(ModelBase):
    __tablename__ = 'products'

    id = Column(Integer, autoincrement=True, primary_key=True)
    productName = Column(String(255), comment="商品名词")
    productMaxPrice = Column(Integer, default=0, comment="商品最大价格")
    productMinPrice = Column(Integer, default=0, comment="商品最小价格")
    productDesc = Column(TEXT, comment="商品描述")
    isHot = Column(Boolean, default=False, comment="热销产品")
    createdTime = Column(DateTime, default=datetime.now, comment="提交时间")
    updatedTime = Column(DateTime, comment="更新时间")

    @classmethod
    def all(cls):
        return dbSession.query(cls).order_by(-cls.createdTime).all()

    @classmethod
    def by_id(cls, _id):
        return dbSession.query(cls).filter(cls.id == _id).first()

    @classmethod
    def hot_product(cls):
        return dbSession.query(cls).filter_by(isHot=True).order_by(-cls.createdTime).all()

    @classmethod
    def paginate(cls, page=1, page_size=10):
        start = page_size * (page - 1)
        end = page * page_size
        return dbSession.query(cls).order_by(-cls.createdTime).slice(start, end).all()

    @property
    def price_range(self):
        return str(self.productMinPrice) + '-' + str(self.productMaxPrice)

    def to_dict(self):
        return {
            "id": self.id,
            "productName": self.productName,
            "productMaxPrice": self.productMaxPrice,
            "productMinPrice": self.productMinPrice,
            "priceRange": self.price_range,
            "productDesc": self.productDesc,
            "isHot": self.isHot,
            "createdTime": format_time(self.createdTime),
            "updatedTime": format_time(self.updatedTime)
        }


class SMSRecord(ModelBase):
    __tablename__ = "sms_record"

    id = Column(Integer, autoincrement=True, primary_key=True)
    phone = Column(String(32), comment="手机号")
    code = Column(String(10), comment="验证码")
    createdTime = Column(Integer, comment="提交时间")

    def is_expired(self):
        """
        :return:  True 过期  False 正常
        """
        now = int(time.time())
        return now - self.createdTime > 1800

    @classmethod
    def verify_code(cls, phone, code):
        row = dbSession.query(cls).filter(cls.phone == phone).first()
        if row:
            if row.is_expired():
                dbSession.delete(row)
                dbSession.commit()
                return False, "您的验证码过期"
            else:
                if row.code == code:
                    dbSession.delete(row)
                    dbSession.commit()
                    return True, "验证成功"
                else:
                    dbSession.delete(row)
                    dbSession.commit()
                    return False, "您的验证码无效, 请重新申请"
        else:
            return False, "您的验证码无效"


class SyStoreModel(ModelBase):
    __tablename__ = "sy_store"

    StoreSn = Column(String(4), primary_key=True)
    OldSn = Column(String(10), comment="老编码")
    StoreName = Column(String(255), comment="门店名称")
    Company = Column(String(100), comment="分公司")
    Address = Column(String(255), comment="地址")
    Lng = Column(Float, comment="经度")
    Lat = Column(Float, comment="纬度")
    Tel = Column(String(100), comment="门店电话")
    MembersDay = Column(Integer, comment="会员日")
    OpenTime = Column(String(255), comment="营业时间")
    InsuranceType = Column(String(255))
    EnbaleSaleGoods = Column(Boolean, default=True, comment="是否可售医保商品")
    IsNeight = Column(Boolean, default=False, comment="夜间营业")
    Status = Column(Boolean, default=True, comment="营业状态")
    CreateTime = Column(DateTime, default=datetime.now, comment="创建时间")
    LastUpdateTime = Column(DateTime, comment="最后更新时间")

    @classmethod
    def by_address(cls, address, limit=10):
        return dbSession.query(cls).filter(cls.Address.like('%{}%'.format(address))).limit(limit)

    @classmethod
    def filter(cls, district, latitude, longitude, limit=10):
        sql = """
            SELECT
                    StoreSn,
                    OldSn,
                    StoreName,
                    Company,
                    Address,
                    Lng,
                    Lat,
                    Tel,
                    MembersDay,
                    OpenTime,
                    InsuranceType,
                    EnbaleSaleGoods,
                    IsNeight,
                    Status,
                    CreateTime,
                    LastUpdateTime,
                    acos(cos({lat}*pi()/180)*cos(Lat*pi()/180)*cos({lng}*pi()/180-Lng*pi()/180)+sin({lat}*pi()/180)*sin(Lat * pi()/180)) *
                        6367000 / 1000 AS distance
                FROM
                    sy_store
                WHERE
                    Address like '%{district}%'
                ORDER BY distance asc 
                LIMIT {limit}
        """.format(**{"district": district, "lat": latitude, "lng": longitude, "limit": limit})
        results = dbSession.execute(sql)
        return cls.result_to_dict(results)

    @staticmethod
    def result_to_dict(results):
        keys = ["StoreSn",
                "OldSn",
                "StoreName",
                "Company",
                "Address",
                "Lng",
                "Lat",
                "Tel",
                "MembersDay",
                "OpenTime",
                "InsuranceType",
                "EnbaleSaleGoods",
                "IsNeight",
                "Status",
                "CreateTime",
                "LastUpdateTime",
                "distance"]
        new_results = []
        raw_results = []
        for res in results:
            new_results.append(res)
        for row in new_results:
            tmp = dict()
            for i in range(len(row)):
                value = row[i]
                key = keys[i]
                if key == 'CreateTime' or key == 'LastUpdateTime':
                    continue
                tmp.setdefault(key, value)
            raw_results.append(tmp)
        return raw_results

    def to_dict(self):
        return {
            "StoreSn": self.StoreSn,
            "OldSn": self.OldSn,
            "StoreName": self.StoreName,
            "Address": self.Address,
            "Tel": self.Tel,
            "Company": self.Company,
            "Lng": self.Lng,
            "Lat": self.Lat,
            "MembersDay": self.MembersDay,
            "OpenTime": self.OpenTime,
            "InsuranceType": self.InsuranceType,
            "EnbaleSaleGoods": self.EnbaleSaleGoods,
            "IsNeight": self.IsNeight,
            "Status": self.Status,
            "CreateTime": format_time(self.CreateTime),
            "LastUpdateTime": format_time(self.LastUpdateTime)
        }
