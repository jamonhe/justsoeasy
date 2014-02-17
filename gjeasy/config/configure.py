#coding=utf8
import os
from gjeasy.config import current_env

LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "log")

LOG_LEVEL = "debug"
if current_env == "development":
    LOG_FILE = "%s/gjeasy.log" % LOG_PATH
else:
    LOG_FILE = "/home/easy/log/gjeasy/gjeasy.log"