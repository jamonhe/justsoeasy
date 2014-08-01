#coding=utf8
import os
from gjeasy.config import current_env

LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "log")

LOG_LEVEL = "debug"
if current_env == "development":
    LOG_FILE = "%s/gjeasy.log" % LOG_PATH
else:
    LOG_FILE = "/home/easy/log/gjeasy/gjeasy.log"

MYSQL_HOST = "www.gjeasy.com"
MYSQL_PORT = 3306
MYSQL_DB = "gjeasy"
MYSQL_USER = "gjeasy"
MYSQL_PASSWORD = "test168"

MONGO_HOST = "23.88.247.190"
MONGO_PORT = 27017
MONGO_DBS = {"news": "news", "weibo": "weibo", "keywords": "keywords"}