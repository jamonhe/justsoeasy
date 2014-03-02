#coding=utf8
from datetime import datetime
import time

def trans_time(str):
    #print str, type(str)
    cur_time= datetime.strptime(str, "%Y-%m-%d %H:%M:%S")
    return int(time.mktime(cur_time.timetuple()))