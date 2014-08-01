#coding=utf8
from datetime import datetime
import time
import traceback
from gjeasy.logger import logger
from gjeasy.models.account_setting import AccountSetting
from gjeasy.models.news import News
from gjeasy.models.weibo import Weibo

from gjeasy.search.baidu_search import search_news
from gjeasy.search.weibo_search import search_weibo
from gjeasy.utils.tranverse_time import trans_time

MAX_LONG_TIME = 500000

def can_send_news(keyword, news_list):
    """
    return new news and last day news
    : keyword:  key word in once search news
    : news_list: news results(a list) of searching , must contain title,content,time,url
    """
    send_news = []
    current_time = int(time.time())
    logger.debug("found %s news" % len(news_list))
    for news in news_list:
        ret, is_created = News.create(keyword, news)
        if not is_created and ret["time"] < current_time - MAX_LONG_TIME:
            break
        send_news.append(news)
    return send_news

def can_send_weibo(name, weibo):
    """
    return new weibo or last day weibo
    : name:  weibo name in once search news
    : weibo: weibo info of searching , must contain name,content,time,url
    """
    current_time = int(time.time())
    ret, is_created = Weibo.create(name, weibo)
    if not is_created and ret["time"] < current_time - MAX_LONG_TIME:
        return None
    return weibo

def get_msg(keyword=None, name=None):
    """
     return grab message and took some filter(如果新闻或微博内容数据库中木有，则返回；
        如果有且发布时间在MAX_LONG_TIME 以内，也返回；其他过滤掉)
    : keyword: key word for searching news
    : name: weibo account
    """
    try:
        if not keyword and not name:
            return {}
        send_contents = {}
        news_list = search_news(keyword)
        send_contents["news"] = can_send_news(keyword, news_list)
        if name:
            weibo = search_weibo(name)
            ret = can_send_weibo(name, weibo)
            if ret:
                send_contents["weibo"] = ret
        return send_contents
    except Exception, e:
        logger.error(traceback.format_exc(e))
        return {}



if __name__=="__main__":
    keywords = [u""]
    result = get_msg(keywords=keywords, name=keywords[0])
    print result
    #print len(result)
    #for ret in result:
    #    print ret["title"], " ", ret["source"], ret["time"]
    #    print "    ", ret["content"], "\n"