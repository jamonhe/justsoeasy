#coding=utf8

from gjeasy.config.configure import MONGO_HOST, MONGO_PORT, MONGO_DBS
from pymongo import MongoClient
from gjeasy.utils.md5 import cal_key

news_conn = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
news_collection = news_conn[MONGO_DBS["news"]]["baidu"]

class News(object):
    """
    : title : news title
    : content: news content
    : url:   news url addr
    : key: content md5
    : imgs: image urls in the content if exist
    : time: news publish time
    """
    def __init__(self, title, content, url, **kwargs):
        self.title = title
        self.content = content
        self.url = url
        self.key = cal_key(content)

    @classmethod
    def create(cls, title, content, url, **kwargs):
        key = cal_key(content)
        news =  {
            "title": title,
            "content": content,
            "url": url,
            "key": key,
        }
        for k, v in kwargs.items():
            news[k] = v
        news_collection.update({"title": title, "key": key}, news, True)