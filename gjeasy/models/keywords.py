#coding=utf8

from gjeasy.config.configure import MONGO_HOST, MONGO_PORT, MONGO_DBS
from pymongo import MongoClient

words_conn = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
words_collection = words_conn[MONGO_DBS["keywords"]]["words"]

class Keywords(object):
    """
    The keywords collection structure(a document):
       "word": keysword ,
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
    def get_words(cls, email_list):
        result = []
        for email in email_list:
            result.append((email, words_collection.find_one({"email": email})))
        return result

if __name__ == "__main__":
    Keywords.add_words("352622654@qq.com", [u"姚贝娜"])