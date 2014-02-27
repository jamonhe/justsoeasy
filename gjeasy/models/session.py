# -*- coding: utf-8 -*-
import contextlib
import traceback
from sqlalchemy.orm import sessionmaker
from gjeasy.models.base import dbs
import kratos.controls.shard
from gjeasy.logger import logger


sessionmakers = [sessionmaker(bind=db) for db in dbs]


def get_router_session():
    """
    连接到router数据库的session
    """
    return get_router_session_maker()()


def get_default_session():
    """
    连到第一个数据库的session
    """
    return sessionmakers[0]()


def get_session(service_id=None, service_name=None):
    """
    :param service_id
    :param service_name
    :return: 存储当前service的数据库的session, 非scoped_session(是否能使用多个scoped_session?)
    """
    if service_id is not None:
        shard_id = Router.route_by_id(service_id)
#        logger.debug('service_id=%d, shard_id=%d' %(service_id, shard_id))
    elif service_name is not None:
        shard_id = Router.route_by_name(service_name)
#        logger.debug("service_name=%s, shard_id=%d"%(service_name, shard_id))
    else:
        raise Exception("Must have service_id or service_name")

    return sessionmakers[shard_id]()


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
def sessionCM(service_id=None, service_name=None):
    """
    :param service_id
    :param service_name
    session 的 contextmanager， 用在with语句
    """
    session = get_session(service_id=service_id, service_name=service_name)
    try:
        yield session
    except Exception, e:
#        logger.warn(traceback.format_exc())
#        session.rollback()
        raise
    finally:
        session.close()


@contextlib.contextmanager
def word_cache_sessionCM():
    session = kratos.controls.shard.word_cache_session()
    try:
        yield session
    except Exception, e:
        logger.warn(traceback.format_exc())
        raise
    finally:
        session.close()

@contextlib.contextmanager
def account_sessionCM():
    session = get_router_session()
    try:
        yield session
    except Exception, e:
        logger.warn(traceback.format_exc())
        raise
    finally:
        session.close()


@contextlib.contextmanager
def human_word_cache_sessionCM():
    session = sessionmakers[0]()
    try:
        yield session
    except Exception, e:
        logger.warn(traceback.format_exc())
        raise
    finally:
        session.close()