#coding=utf8

from sqlalchemy import Column, Integer,String
from gjeasy.config.configure import MYSQL_DB, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_PORT, MYSQL_USER
from gjeasy.controls.base import Base


class ACCOUNT_FORMAT_EXCEPTION():
    def __init__(self):
        pass


class Account(Base):
    __tablename__ = "account"
    id = Column("id", Integer, primary_key=True)
    email = Column("email", String(50), index=True)
    phone = Column("phone", String(20), index=True)
    passwd = Column("passwd", String(20), index=True)

    def __init__(self, email=None, phone=None, passwd=""):
        if email is None and phone is None:
            raise ACCOUNT_FORMAT_EXCEPTION()
        self.email = email
        self.phone = phone
        self.passwd = passwd

