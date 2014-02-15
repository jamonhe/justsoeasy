#coding=utf8

import smtplib
from email.mime.text import MIMEText
import traceback
from urlparse import unquote

default_mail_param = {
    "mail_host": "smtp.exmail.qq.com",
    "mail_user": "gjeasy",
    "mail_pass": "qiongo16739",
    "mail_postfix": "xingcloud.com",
}


def send_mail(to_list, subject, content, mail_param=default_mail_param):
    me = "hello" + "<" + mail_param["mail_user"] + "@" + mail_param["mail_postfix"] + ">"
    #me = "<" + "hehuilin" + "@" + "xingcloud.com" + ">"
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
        print str(e)
        print traceback.format_exc(e)
        return False

if __name__ == "__main__":
    to_mail = ["352622654@qq.com"]
    if send_mail(to_mail, "Yao bei na", "gjeasy test"):
        print "发送成功"
    else:
        print "发送失败"
    #print unquote("%25E5%25A7%259A%25E8%25B4%259D%25E5%25A8%259C")