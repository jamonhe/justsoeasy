#coding: utf8

__author__="hhl"



import urllib
import urllib2
import cookielib
import mechanize
from BeautifulSoup import BeautifulSoup
from datetime import datetime
import time

BAIDU_BASE_URL = {
    "news": "http://news.baidu.com/ns?",
}

def search_news(keywords=[], num=5):
    if not keywords:
        return
    #print keywords
    br = mechanize.Browser()
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]


    encode_words = [urllib.quote(word.encode("utf-8")) for word in keywords]
    search_words = "+".join(encode_words)
    url = "%sword=%s" % (BAIDU_BASE_URL["news"], search_words)
    #print url
    result = br.open(url).read()

    soup = BeautifulSoup(result)
    news_list = []
    for c in soup.findAll("li"):
        news = {}
        news["title"] = c.a.text.strip()
        news["addr"] = c.a.get("href")
        news["source"], news["time"] = c.span.text.replace("&nbsp;", " ").strip().split(" ", 1)
        news["content"] = c.find("div", {"class": "c-summary"}).text\
            .replace(u"&nbsp;百度快照", "").strip()
        news_list.append(news)

    return news_list



if __name__=="__main__":
    keywords = [u"姚贝娜", u"春晚"]
    result = search_news(keywords=keywords)
    print len(result)
    for ret in result:
        print ret["title"], " ", ret["source"]
        print ret["time"]
        print "    ", ret["content"], "\n"

    #str = "2014-02-13 10:33:00"
    #