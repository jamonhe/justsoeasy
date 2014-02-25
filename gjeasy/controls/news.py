#coding=utf8

from gjeasy.config.configure import MONGO_HOST, MONGO_PORT, MONGO_DBS
from pymongo import MongoClient

news_conn = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
news_db = news_conn[MONGO_DBS["news"]]

class News(object):

    def __init__(self, title, content, url, **kwargs):
        self.title = title
        self.content = content
        self.url = url

    @classmethod
    def create(cls, title, content, url, **kwargs):
        pass