#coding=utf8
from datetime import datetime
import time

from gjeasy.search.baidu_search import search_news
from gjeasy.search.weibo_search import search_weibo


def trans_time(str):
    cur_time= datetime.strptime(str, "%Y-%m-%d %H:%M:%S")
    return int(time.mktime(cur_time.timetuple()))

def get_msg(keywords=[], name=None, interval=200000):
    news_list = search_news(keywords)
    cur_time = int(time.time())
    send_news = []
    print news_list
    for news in news_list:
        if cur_time - trans_time(news["time"]) < interval:
            send_news.append("%s    %s %s \n   %s\n   %s" %
                             (news["title"], news["source"], news["time"], news["content"], news["addr"]))

    send_contents = "\n\n".join(send_news)

    if name:
        weibo= search_weibo(name)
        if cur_time - trans_time(weibo["time"]) < interval:
            send_weibo_content = "%s %s %s \n   %s" % (name, weibo["addr"], weibo["time"], weibo["content"])
            send_contents += send_weibo_content
    return send_contents



if __name__=="__main__":
    keywords = [u""]
    result = get_msg(keywords=keywords, name=keywords[0])
    print result
    #print len(result)
    #for ret in result:
    #    print ret["title"], " ", ret["source"], ret["time"]
    #    print "    ", ret["content"], "\n"