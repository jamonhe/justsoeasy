#coding=utf8

from gjeasy.config.configure import MONGO_HOST, MONGO_PORT, MONGO_DBS
from pymongo import MongoClient

words_conn = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
words_collection = words_conn[MONGO_DBS["keywords"]]["words"]

class Keywords(object):

    @classmethod
    def add_words(cls, email, add_word_list):
        ori_words = words_collection.find_one({"email": email}, fields={"word_list": 1, "_id": -1})
        ori_word_list = ori_words.get("word_list", []) if ori_words else []
        new_word_list = list(set(ori_word_list).union(add_word_list))
        words_collection.update({"email": email}, {"$set": {"word_list": new_word_list}}, True)


if __name__ == "__main__":
    Keywords.add_words("352622654@qq.com", [u"姚贝娜"])