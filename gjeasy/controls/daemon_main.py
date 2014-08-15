#coding=utf8
import time
from gjeasy.controls.get_msg import get_msg
from gjeasy.controls.send_msg import send_msg
from gjeasy.emails.send_mail import send_mail
from gjeasy.models.account import Account
from gjeasy.models.account_setting import AccountSetting
from gjeasy.models.keywords import Keywords


def daemon_main(interval=300):
    """
    1. 获取所有需要翻译的keywords, 分级别：5分钟，2分钟等，默认五分钟 ;
    2. 搜寻百度、微博等最新消息 ;
    3. 验证待发送的email_list;
    3. 根据keywords注册的email_list将最新消息内容发送给相应email用户;
    4. 将内容存入mongo中的content数据库;
    """
    words_emails = Keywords.get_search_words(interval)
    print "word_emails=", words_emails
    for word, emails in words_emails:
        AccountSetting.update_search_time(emails, word, time.time())
        latest_content = get_msg(word, word)
        print "content", latest_content
        send_msg(emails, word, word, latest_content)

if __name__ == "__main__":
    daemon_main()