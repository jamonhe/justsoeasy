#coding=utf8
from datetime import datetime
import time
from gjeasy import logger
from gjeasy.emails.send_mail import send_mail
from gjeasy.models.account_setting import AccountSetting
from gjeasy.utils.tranverse_time import trans_time


def need_send_news(email, keyword, news_list):
    """
    根据消息发布时间查询数据库，判断该消息是否需要发送，
    若发布时间>=数据库中该用户keyword的最后一次搜索时间，且最后一次发送时间>=最后一次搜索时间，则发送；
    : keyword:  key word in once search news
    : news_list: news results(a list) of searching , must contain title,content,time,url
    """
    need_send_news = []
    last_search_time, last_email_time = AccountSetting.get_last_time(email, keyword)
    for news in news_list:
        if last_search_time <= trans_time(news["time"]) and last_search_time >= last_email_time:
            need_send_news.append(news)

        #send_news.append("%s    %s %s \n   %s\n   %s" %
        #                 (news["title"], news["source"], news["time"], news["content"], news["url"]))
    return need_send_news

def need_send_weibo(email, name, weibo):
    """
    return new weibo or last day weibo
    : name:  weibo name in once search news
    : weibo: weibo info of searching , must contain name,content,time,url
    """
    need_send_weibo = {}
    last_search_time, last_email_time = AccountSetting.get_last_time(email, name)
    if last_search_time <= trans_time(weibo["time"]) and last_search_time >= last_email_time:
        return weibo
    return {}

    #return "%s %s %s \n   %s" % (name, weibo["url"], weibo["time"], weibo["content"])

def gen_news_str(news_list):
    return "<br><br>".join(
        ['<a href="%s"> %s </a>    %s %s <br>   %s<br>' %
         (news["url"], news["title"], news["source"], news["time"], news["content"]) for news in news_list
        ])

def gen_weibo_str(name, weibo):
    return "%s %s %s \n   %s" % (name, weibo["url"], weibo["time"], weibo["content"])

def send_msg(email_list, keyword, name, content):
    """
    : keyword: key word for searching news
    : name: weibo account
    : content : a dict contain search results, such as {"news"[news1, news2], "weibo": weibo}
    """
    for email in email_list:
        if content.has_key("news") and content["news"]:
            send_news = need_send_news(email, keyword, content["news"])
            if send_news:
                news_str = gen_news_str(send_news)
                subject = "%s 有新消息了^-^" % '+'.join(keyword)
                cur_time = int(time.time())
                send_mail(email, subject, news_str)
                AccountSetting.update_email_time(email, keyword, cur_time)

        if content.has_key("weibo") and content["weibo"]:
            send_weibo = need_send_weibo(email, name, content["weibo"])
            if send_weibo:
                weibo_str = gen_weibo_str(name, send_weibo)
                subject = keyword + " 有新的微博动态了^-^"
                send_mail(email, subject, news_str)
                cur_time = int(time.time())
                AccountSetting.update_email_time(email, name, cur_time)