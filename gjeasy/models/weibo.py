#coding=utf8

from gjeasy.config.configure import MONGO_HOST, MONGO_PORT, MONGO_DBS
from pymongo import MongoClient
from gjeasy.utils.md5 import cal_key

weibo_conn = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
weibo_collection = weibo_conn[MONGO_DBS["weibo"]]["sina"]


class Weibo(object):

    def __init__(self, name, content, url, **kwargs):
        self.name = name
        self.content = content
        self.url = url

    @classmethod
    def create(cls, name, content, url, **kwargs):
        key = cal_key(content)
        weibo =  {
            "name": name,
            "content": content,
            "url": url,
            "key": key,
        }
        for k, v in kwargs.items():
            weibo[k] = v
        weibo_collection.update({"name": name, "key": key}, weibo, True)