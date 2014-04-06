#coding=utf8

from celery import Celery
from celery.schedules import crontab
from datetime import timedelta
from kombu import Queue, Exchange


class BaseConfig(object):
    CELERY_ACKS_LATE = True
    CELERY_TIMEZONE = 'Asia/Shanghai'
    BROKER_URL = "amqp://gjeasy:gjeasy168@115.29.142.18:5672//"
    CELERY_QUEUES = (
        Queue('grab_msg', Exchange('grab_msg'), routing_key='grab_msg'),
    )

    CELERY_ROUTES = {
        "gjeasy.tasks.period_task.grab_msg": {
            "routing_key": "grab_msg",
            "queue": "grab_msg",
        },
    }

    CELERY_IMPORTS = (
        'gjeasy.tasks.period_task',
    )

    CELERYBEAT_SCHEDULE = {
        "grab_msg": {
        "task": "gjeasy.tasks.period_task.grab_msg",
        "schedule": timedelta(seconds=300),
        "args": ()
     },
    }



celery = Celery()
celery.config_from_object(BaseConfig)