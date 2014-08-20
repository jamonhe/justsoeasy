#coding=utf8

from gjeasy.config.configure import MONGO_HOST, MONGO_PORT, MONGO_DBS
from pymongo import MongoClient
from gjeasy.utils.coding_str import str2utf8
from gjeasy.utils.md5 import cal_key

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
    def add_words(cls, email, add_word_list, interval=300):
        """
         add new search words for one email
        """
        add_word_list = [str2utf8(word)[0] for word in add_word_list]
        words_key = cal_key(','.join(add_word_list))


        ret = words_collection.find_one({"key": words_key})
        if not ret:
            words_collection.insert({"word": add_word_list, "email_list": [email], "key": words_key,"interval": interval})
        elif ret and email in set(ret.get("email_list")):
            pass
        else:
            ret = words_collection.find_one({"key": words_key})

            words_collection.update({"key": words_key}, {"$set": {"email_list": ret["email_list"].append(email)}})
        # for word in add_word_list:
        #     ret = words_collection.find_one({"word": word})
        #     if not ret:
        #         words_collection.insert({"word": word, "email_list": [email], "interval": interval})
        #         continue
        #     if ret and email in set(ret.get("email_list")):
        #         continue
        #     else:
        #         words_collection.update({"word": word}, {"$set": {"email_list": ret["email_list"].append(email)}})

        return True


    @classmethod
    def get_search_words(cls, interval=300):
        result =[(word.get("word"), word.get("email_list")) for word in words_collection.find({"interval": 300})]

        return result

if __name__ == "__main__":
    Keywords.add_words("352622654@qq.com", [u"成龙"])
