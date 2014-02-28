# coding=utf8

import traceback
import smtplib
import logging
import socket
from email.mime.text import MIMEText

from kratos.tasks import celery
from kratos.setting import USE_EMAIL_NOTIFY, TO_EMAIL_ADDRS, TIMEOUT


emails = [
        {
            'account': 'xcmonitor01@163.com',
            'password': 'xingcloud',
        },
        {
            'account': 'xcmonitor02@163.com',
            'password': 'xingcloud',
        },
        {
            'account': 'xcmonitor03@163.com',
            'password': 'xingcloud',
        },
        {
            'account': 'xcmonitor04@163.com',
            'password': 'xingcloud',
        },
        {
            'account': 'xcmonitor05@163.com',
            'password': 'xingcloud',
        },
        {
            'account': 'xcmonitor06@163.com',
            'password': 'xingcloud',
        },
        {
            'account': 'xcmonitor07@163.com',
            'password': 'xingcloud',
        },
]


emailCount = 0


def getEmailSetting():
    global emails, emailCount
    emailCount = (emailCount + 1) % len(emails)
    return emails[emailCount]


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))  #connect to google open dns
    except socket.error:
        ret = ''
    finally:
        ret =  s.getsockname()[0]
        s.close()
    return ret

ip = get_ip()

class SendMail:
    def __init__(self, to_list):
        self.to_list = to_list


    def send(self, subject, content, _subtype='plain'):
        msg = MIMEText(content, _subtype=_subtype, _charset='utf8')

        try:
            s = smtplib.SMTP("smtp.163.com", 25, timeout=TIMEOUT)
            s.ehlo()
            s.starttls()
            s.ehlo()
            setting = getEmailSetting()
            account = setting['account']
            password = setting['password']
            self.me = 'Kratos<' + account + '>'
            msg['Subject'] = subject
            msg['From'] = self.me
            msg['To'] = self.to_list
            s.login(account, password)
            s.sendmail(self.me, self.to_list.split(','), msg.as_string())
            s.close()

            return True
        except Exception, e:
            print traceback.format_exc()
            return False


@celery.task(ignore_result=True)
def send_mail_task(to_list, subject, content, _subtype='plain'):
    print 'sending'
    m = SendMail(to_list)
    m.send(subject, content, _subtype)


class EmailHandler(logging.Handler):

    def __init__(self, delay = True):
        logging.Handler.__init__(self)

        self.delay = delay
        self.setLevel(logging.ERROR)
        self.formatter = logging.Formatter("%(asctime)s\t%(process)d|%(thread)d\t%(levelname)s\t%(module)s\t%(funcName)s:%(lineno)d\t%(message)s", "%Y-%m-%d@%H:%M:%S")
        self.title_formatter = logging.Formatter("%(levelname)s\t%(module)s", "%Y-%m-%d@%H:%M:%S")


    def emit(self, record):
        if USE_EMAIL_NOTIFY:
            to_list = ','.join([v for k, v in TO_EMAIL_ADDRS])
            if self.delay:
                send_mail_task.delay(to_list, '%s: %s' % (ip, self.title_formatter.format(record)), self.formatter.format(record))
            else:
                send_mail_task(to_list, '%s: %s' % (ip, self.title_formatter.format(record)), self.formatter.format(record))


if __name__ == '__main__':
    logger = logging.getLogger('TestLogger')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(EmailHandler())
    logger.debug("This is a test message.")
    logger.info("This is a test message.")
    logger.warn("This is a test message.")
    logger.error("This is a test message.")
