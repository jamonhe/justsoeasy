#coding=utf8

from gjeasy.config.configure import MONGO_HOST, MONGO_PORT, MONGO_DBS
from pymongo import MongoClient
from gjeasy.utils.md5 import cal_key
from gjeasy.utils.tranverse_time import trans_time

news_conn = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
news_collection = news_conn[MONGO_DBS["news"]]["baidu"]

class News(object):
    """
    primary key : consist of (keywords, key)
    : keyword : search keywords
    : title : news title
    : content: news content
    : url:   news url addr
    : key: content md5
    : imgs: image urls in the content if exist
    : time: news publish time
    """
    def __init__(self, keyword, title, content, url, **kwargs):
        self.keyword = keyword
        self.title = title
        self.content = content
        self.url = url
        self.key = cal_key(content)

    @classmethod
    def create(cls, keyword, add_news):
        """
        : add_news : a dict which must contain : title, content, url, time; may content source, ...
        """
        key = cal_key(add_news["content"])
        ret = news_collection.find_one({"keyword": keyword, "key": key})
        if ret:
            return ret, False
        news = {
            "keyword": keyword,
            "title": add_news["title"],
            "content": add_news["content"],
            "url": add_news["url"],
            "key": key,
        }
        news.update(add_news)
        news["time"] = trans_time(news["time"])
        news_collection.insert(news)
        return news, True