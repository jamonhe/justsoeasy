#coding=utf8
from gjeasy.controls.get_messages import get_msg
from gjeasy.emails.send_mail import send_mail
from gjeasy.models.account import Account
from gjeasy.models.keywords import Keywords


def process_messages():
    """
    1. 获取所有需要翻译的keywords, 分级别：5分钟，2分钟等，默认五分钟 ;
    2. 搜寻百度、微博等最新消息 ;
    3. 验证待发送的email_list;
    3. 根据keywords注册的email_list将最新消息内容发送给相应email用户;
    4. 将内容存入mongo中的content数据库;
    """
    need_emails = Account.get_avail_account()
    email_words = Keywords.get_words(need_emails)
    for email, words in email_words:
        latest_content = get_msg(words, words)
        subject = ",".join(words) + "最新消息"
        send_mail(email, subject, latest_content)