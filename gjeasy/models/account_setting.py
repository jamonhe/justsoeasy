#coding=utf8
from sqlalchemy import BIGINT, String, Integer, Column, ForeignKey, Sequence
from sqlalchemy.orm import relationship
from gjeasy.models.base import Base
from gjeasy.models.session import sessionCM


class AccountSetting(Base):
    __tablename__ = "account_setting"
    __table_args__ = {"mysql_engine": "InnoDB"}

    id = Column(Integer, Sequence("setting_id_seq"), primary_key=True)
    email = relationship("Account", backref="keywords", order_by="Account.email")

    keyword = Column(String(100), nullable=False, index=True)

    #搜索的间隔
    interval = Column(Integer, default=300)
    #最近一次搜索时间
    searched_time = Column(Integer, default=0)
    #最近一次发送邮件的时间
    emailed_time = Column(Integer, default=0)

    def __init__(self, email, keyword, **kwargs):
        self.email = email
        self.keyword = keyword

    @classmethod
    def add_words(cls, email, add_word_list):
        """
         add new search words for one email
        """
        with sessionCM() as session:
            ret = session.query(AccountSetting).filter_by(email=email)\
                .filter(AccountSetting.keyword._in(add_word_list)).all()
            exist_words = [a.word for a in ret]
            need_add_words = list(set(add_word_list) - set(exist_words))
            for word in need_add_words:
                new_setting = cls(email=email, keyword=word)
                session.add(new_setting)
                session.commit()

        return True

    @classmethod
    def update_search_time(cls, email_list, keyword, timestamp):
        """
        update searched_time
        """
        with sessionCM() as session:
            for email in email_list:
                account_setting = session.query(AccountSetting).filter_by(email=email, keyword=keyword).first()
                account_setting.searched_time = timestamp
                session.commit()

    @classmethod
    def update_email_time(cls, email, keyword, timestamp):
        """
        update emailed_time
        """
        with sessionCM() as session:
            account_setting = session.query(AccountSetting).filter_by(email=email, keyword=keyword).first()
            account_setting.emailed_time = timestamp
            session.commit()

    @classmethod
    def get_last_time(cls, email, keyword):
        """
         return searched_time, emailed_time
        : email: AccountSetting email
        : keyword: key word of search news/weibo... ,
        : timestamp: timestamp of search result
        """
        with sessionCM() as session:
            ret = session.query(AccountSetting).filter_by(email=email, keyword=keyword).first()
            return ret.searched_time, ret.emailed_time


if __name__ == "__main__":
    AccountSetting.add_words("352622654@qq.com", [u"姚贝娜"])