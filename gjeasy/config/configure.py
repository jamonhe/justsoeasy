#coding=utf8
import os
from gjeasy.config import current_env, DOMAIN_IP

# LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "log")
LOG_PATH = "/home/gjeasy/log"

LOG_LEVEL = "debug"
if current_env == "development":
    LOG_FILE = "%s/gjeasy.log" % LOG_PATH
else:
    LOG_FILE = "/home/easy/log/gjeasy/gjeasy.log"

MYSQL_HOST = DOMAIN_IP #"www.gjeasy.com"
MYSQL_PORT = 52013
MYSQL_DB = "gjeasy"
MYSQL_USER = "gjeasy"
MYSQL_PASSWORD = "test168"

MONGO_HOST = DOMAIN_IP
MONGO_PORT = 52014
MONGO_DBS = {"news": "news", "weibo": "weibo", "keywords": "keywords"}