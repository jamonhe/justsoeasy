#coding=utf8
from datetime import datetime
import time
import traceback
from gjeasy.logger import logger
from gjeasy.models.news import News
from gjeasy.models.weibo import Weibo

from gjeasy.search.baidu_search import search_news
from gjeasy.search.weibo_search import search_weibo
from gjeasy.utils.tranverse_time import trans_time

MAX_LONG_TIME = 100000

def need_send_news(keyword, news_list):
    """
    return new news and last day news
    : keyword:  key word in once search news
    : news_list: news results(a list) of searching , must contain title,content,time,url
    """
    send_news = []
    current_time = time.time()
    logger.debug("found %s news" % len(news_list))
    for news in news_list:
        ret, is_created = News.create(keyword, news)
        ret["time"] = trans_time(ret.get("time"))
        if not is_created and ret["time"] < current_time - MAX_LONG_TIME:
            break
        send_news.append("%s    %s %s \n   %s\n   %s" %
                         (news["title"], news["source"], news["time"], news["content"], news["url"]))
    return search_news

def need_send_weibo(name, weibo):
    """
    return new weibo or last day weibo
    : name:  weibo name in once search news
    : weibo: weibo info of searching , must contain name,content,time,url
    """
    ret, is_created = Weibo.create(name, weibo)
    if cur_time - trans_time(weibo["time"]) < interval:
        send_weibo_content = "%s %s %s \n   %s" % (name, weibo["addr"], weibo["time"], weibo["content"])

def get_msg(keyword=None, name=None, interval=200000):
    try:
        if not keyword and not name:
            return ""
        news_list = search_news(keyword)
        cur_time = int(time.time())

        send_contents = "\n\n".join(need_send_news(keyword, news_list))

        if name:
            weibo= search_weibo(name)
            send_contents += send_weibo_content
        return send_contents
    except Exception, e:
        logger.error(traceback.format_exc(e))
        return "Null"



if __name__=="__main__":
    keywords = [u""]
    result = get_msg(keywords=keywords, name=keywords[0])
    print result
    #print len(result)
    #for ret in result:
    #    print ret["title"], " ", ret["source"], ret["time"]
    #    print "    ", ret["content"], "\n"