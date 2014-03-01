#coding=utf8
from gjeasy.emails import send_mail
from gjeasy.controls.get_msg import get_msg


key_word = [u"姚贝娜"]
test_email = "352622654@qq.com"

def grab_msg(keywords=key_word, name=u"姚贝娜", interval=2000, to_mail=test_email):
    send_contents = get_msg(keywords=keywords, name=name, interval=interval)
    if send_contents:
        send_mail(test_email, "gjeasy grab info", send_contents)
