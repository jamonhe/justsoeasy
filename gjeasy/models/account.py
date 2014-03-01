#coding=utf8

from sqlalchemy import Column, Integer,String, BIGINT, SMALLINT
from gjeasy.config.configure import MYSQL_DB, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_PORT, MYSQL_USER
from gjeasy.models.base import Base
from gjeasy.models.session import sessionCM


class ACCOUNT_FORMAT_EXCEPTION():
    def __init__(self):
        pass


class Account(Base):
    __tablename__ = "account"

    #id = Column(BIGINT(unsigned=True), )
    email = Column(String(50), nullable=False, unique=True, primary_key=True)
    phone = Column(String(20), index=True)
    passwd = Column(String(20))

    AVAIL, SHUT = range(2)
    status = Column(SMALLINT, default=AVAIL)

    def __init__(self, email=None, phone=None, passwd=""):
        if email is None and phone is None:
            raise ACCOUNT_FORMAT_EXCEPTION()
        self.email = email
        self.phone = phone
        self.passwd = passwd

    @classmethod
    def create(cls, email, phone, passrd):
        new_account = cls(email, phone, passrd)
        with sessionCM() as session:
            session.add(new_account)
            session.commit()

    @classmethod
    def get_avail_account(cls):
        with sessionCM() as session:
            return session.query(Account.email).filter_by(status=cls.AVAIL).all()


if __name__ == "__main__":
    from gjeasy.models.base import metadata
    print metadata.sorted_tables[0].name
    print len(metadata.sorted_tables)
    #Account.create("352622654@qq.com", "13476261942", "test168")