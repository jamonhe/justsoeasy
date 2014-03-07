#coding=utf8
from gjeasy.config.celeryconfig import celery
from gjeasy.controls.daemon_main import daemon_main



key_word = [u"姚贝娜"]
test_email = "352622654@qq.com"

@celery.task(ignore_result=True)
def grab_msg(keywords=key_word, name=u"姚贝娜", interval=300, to_mail=test_email):
    daemon_main()
