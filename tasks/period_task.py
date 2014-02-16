#coding=utf8
from emails.send_mail import send_mail
from views.base import get_msg


key_word = [u"姚贝娜"]

def grab_msg(keywords=key_word, name=u"姚贝娜", interval=2000):
    send_conents = get_msg(keywords=keywords, name=name, interval=interval)
    if send_contents:
        send_mail("352622654@qq.com", "gjeasy grab info", send_contents)
