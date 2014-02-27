#coding=utf8

from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as SA
import datetime
from sqlalchemy.orm import object_session
from gjeasy.config.configure import MYSQL_DB, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_PORT, MYSQL_USER

class tBase(object):
    session = property(lambda self: object_session(self))
    created_date = SA.Column(SA.DateTime, default = datetime.datetime.now)
    modified_date = SA.Column(SA.DateTime, default = datetime.datetime.now, onupdate=SA.text('current_timestamp'))

Base = declarative_base(cls=tBase)
metadata = Base.metadata

#: 是否在标准输出流打印sql语句(sqlalchemy)
echo = False
mysql_db = SA.create_engine(
        'mysql://%s:%s@%s/%s?charset=utf8' % (MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DB),
        echo=echo,
        pool_recycle=3600,
        pool_size=15
    )
