#coding=utf8

from gjeasy.config.configure import MONGO_HOST, MONGO_PORT, MONGO_DBS
from pymongo import MongoClient

words_conn = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
words_collection = words_conn[MONGO_DBS["keywords"]]["words"]

class Keywords(object):
    """
    The keywords collection structure(a document):
       "word": keysword ,
       "key": ... ，               # md5 of keyword
       "interval": 300, 120, ...   #搜索的最短时间间隔
       "last_time": 13...         # timestamp, 最后一次的搜索时间
       "email_list": [ , ]
    """
    @classmethod
    def add_words(cls, email, add_word_list):
        """
         add new search words for one email
        """
        for word in add_word_list:
            ret = words_collection.find_one({"word": word})
            if email in set(ret["email_list"]):
                break
            else:
                words_collection.update({"word": word}, {"$set": {"email_list": ret["email_list"].append(email)}})

        return True


    @classmethod
    def get_search_words(cls, interval=300):
        result =[ (word.get("word"), word.get("email_list")) for word in words_collection.find({"interval": 300}) ]

        return result

if __name__ == "__main__":
    Keywords.add_words("352622654@qq.com", [u"姚贝娜"])