#coding=utf8

from celery import Celery
from celery.schedules import crontab
from kombu import Queue, Exchange


class BaseConfig(object):
    CELERY_ACKS_LATE = True
    CELERY_TIMEZONE = 'Asia/Shanghai'
    BROKER_URL = "amqp://gjeasy:gjeasy168@115.29.142.18:5672//"
    CELERY_QUEUES = (
        Queue('dnfs_stat', Exchange('dnfs_stat'), routing_key='dnfs.stat'),
        Queue('dnfs_file_delete', Exchange('dnfs_file_delete'), routing_key='dnfs.file.delete'),

    )

    CELERY_ROUTES = {
        "dnfs.tasks.xc_stat.xc_stat": {
            "routing_key": "dnfs.stat",
            "queue": "dnfs_stat",
        },
        "dnfs.tasks.file_operate.file_delete": {
            "routing_key": "dnfs.file.delete",
            "queue": "dnfs_file_delete",
        },
    }

    CELERY_IMPORTS = (
        'dnfs.tasks.xc_stat',
        'dnfs.tasks.file_operate',
    )

    CELERYBEAT_SCHEDULE = {
    }

    #: Email相关设置
    CELERY_SEND_TASK_ERROR_EMAILS = True
    ADMINS = (
        ('hehuilin', 'hehuilin@xingcloud.com'),
    )
    SERVER_EMAIL = 'GJEASY stat info<xcmonitor01@163.com>'
    EMAIL_HOST = 'smtp.163.com'
    EMAIL_HOST_USER = 'xcmonitor01@163.com'
    EMAIL_HOST_PASSWORD = 'xingcloud'
    EMAIL_PORT = 25
    EMAIL_USE_TLS = True
    EMAIL_TIMEOUT = 10

celery = Celery()
celery.config_from_object(BaseConfig)