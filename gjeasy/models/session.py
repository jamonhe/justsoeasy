# -*- coding: utf-8 -*-
import contextlib
import traceback
from sqlalchemy.orm import sessionmaker
from gjeasy.models.base import mysql_db
from gjeasy.logger import logger


sessionmakers = sessionmaker(bind=mysql_db)



def get_session(service_id=None, service_name=None):
    """
    :param service_id
    :param service_name
    :return: 存储当前service的数据库的session, 非scoped_session(是否能使用多个scoped_session?)
    """

    return sessionmakers()


@contextlib.contextmanager
def all_session():
    session_list = []

    def session_gen():
        for sm in sessionmakers:
            session = sm()
            session_list.append(session)
            yield session
    try:
        yield session_gen()
    except Exception:
        logger.warn(traceback.format_exc())
        raise
    finally:
        for s in session_list:
            s.close()


@contextlib.contextmanager
def sessionCM():
    """
    :param service_id
    :param service_name
    session 的 contextmanager， 用在with语句
    """
    session = get_session()
    try:
        yield session
    except Exception, e:
#        logger.warn(traceback.format_exc())
#        session.rollback()
        raise
    finally:
        session.close()
