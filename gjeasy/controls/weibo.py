#coding=utf8

from gjeasy.config.configure import MONGO_HOST, MONGO_PORT, MONGO_DBS
from pymongo import MongoClient

weibo_conn = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
weibo_db = weibo_conn[MONGO_DBS["weibo"]]


class Weibo(object):

    def __init__(self, name, content, url, **kwargs):
        self.name = name
        self.content = content
        self.url = url

    @classmethod
    def create(cls, title, content, url, **kwargs):
        pass