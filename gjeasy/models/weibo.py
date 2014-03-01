#coding=utf8

from gjeasy.config.configure import MONGO_HOST, MONGO_PORT, MONGO_DBS
from pymongo import MongoClient
from gjeasy.utils.md5 import cal_key
from gjeasy.utils.tranverse_time import trans_time

weibo_conn = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
weibo_collection = weibo_conn[MONGO_DBS["weibo"]]["sina"]


class Weibo(object):
    """
    primary key : consist of (name, key)
    : name : search keywords
    : content: news content
    : url:   news url addr
    : key: content md5
    : time: news publish time
    """

    def __init__(self, name, content, url, **kwargs):
        self.name = name
        self.content = content
        self.url = url
        self.key = cal_key(content)

    @classmethod
    def create(cls, name, add_weibo):
        """
        : add_weibo : a dict which must contain : content, url, time; may content  ...
        """
        key = cal_key(add_weibo["content"])
        ret = weibo_collection.find_one({"name": name, "key": key})
        if ret:
            return ret, False
        weibo =  {
            "name": name,
            "content": add_weibo["content"],
            "url": add_weibo["url"],
            "key": key,
        }
        weibo.update(add_weibo)
        weibo["time"] = trans_time(weibo["time"])
        weibo_collection.insert(weibo)
        return weibo, True