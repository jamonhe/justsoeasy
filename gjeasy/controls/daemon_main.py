#coding=utf8
from gjeasy.controls.get_messages import get_msg
from gjeasy.emails.send_mail import send_mail
from gjeasy.models.account import Account
from gjeasy.models.keywords import Keywords


def process_messages():
    need_emails = Account.get_avail_account()
    email_words = Keywords.get_words(need_emails)
    for email, words in email_words:
        latest_content = get_msg(words, words)
        subject = ",".join(words) + "最新消息"
        send_mail(email, subject, latest_content)