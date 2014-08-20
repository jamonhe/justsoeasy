#coding=utf8
import os
from gjeasy.config import current_env, DOMAIN_IP

LOG_LEVEL = "debug"
if current_env == "development":
    LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "log")
    MAIN_PORT = 8880
else:
    LOG_PATH = "/home/gjeasy/log"
    MAIN_PORT = 80

LOG_FILE = "%s/gjeasy.log" % LOG_PATH

MYSQL_HOST = DOMAIN_IP #"www.gjeasy.com"
MYSQL_PORT = 52013
MYSQL_DB = "gjeasy"
MYSQL_USER = "gjeasy"
MYSQL_PASSWORD = "test168"

MONGO_HOST = DOMAIN_IP
MONGO_PORT = 52014
MONGO_DBS = {"news": "news", "weibo": "weibo", "keywords": "keywords"}