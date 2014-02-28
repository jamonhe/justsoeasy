#coding=utf8
from sqlalchemy import BIGINT, String, Integer
from xlwt import Column

from gjeasy.config.configure import MONGO_HOST, MONGO_PORT, MONGO_DBS
from pymongo import MongoClient

words_conn = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
words_collection = words_conn[MONGO_DBS["keywords"]]["words"]

class AccountSetting(object):
    __tablename__ = "account_setting"
    id = Column(BIGINT(unsigned=True), primary_key=True)
    email = Column(String(50), nullable=False, unique=True, index=True)

    #搜索的间隔
    interval = Column(Integer, default=300)
    #最近一次发送邮件的时间
    emailed_time = Column(BIGINT(unsigned=True))

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