#coding=utf8

import smtplib
from email.mime.text import MIMEText
import traceback
from urlparse import unquote
from gjeasy import logger

default_mail_param = {
    "mail_host": "smtp.exmail.qq.com",
    "mail_user": "info@gjeasy.com",
    "mail_pass": "test168",
    "mail_postfix": "gjeasy.com",
}


def send_mail(to_list, subject, content, mail_param=default_mail_param):
    me = "<" + mail_param["mail_user"].rsplit("@", 1)[0] + "@" + mail_param["mail_postfix"] + ">"
    msg = MIMEText(content, _subtype='plain', _charset='utf8')
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        server = smtplib.SMTP()
        server.connect(mail_param["mail_host"])
        server.login(mail_param["mail_user"], mail_param["mail_pass"])
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception, e:
        logger.error(traceback.format_exc(e))
        return False

if __name__ == "__main__":
    to_mail = ["352622654@qq.com"]
    if send_mail(to_mail, "Yao bei na", "gjeasy test \n Yao"):
        print "发送成功"
    else:
        print "发送失败"

    #print '\xc7\xeb\xb5\xc7\xc2\xbc\xd0\xde\xb8\xc4\xc3\xdc\xc2\xeb'.decode("utf-8")