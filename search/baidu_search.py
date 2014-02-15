#coding: utf8

__author__="hhl"



import urllib
import urllib2
import cookielib
import mechanize
from BeautifulSoup import BeautifulSoup

BAIDU_BASE_URL = {
    "news": "http://news.baidu.com/ns?",
}

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

def search_news(keywords=[], num=5):
    if not keywords:
        return

    encode_words = [urllib.quote(word) for word in keywords]
    search_words = "+".join(encode_words)
    url = "%sword=%s" % (BAIDU_BASE_URL["news"], search_words)
    print url
    result = br.open(url).read()
    print "************************\n"
    soup = BeautifulSoup(result)
    news_list = []
    for c in soup.findAll("li"):
        news = {}
        news["title"] = c.a.text.strip()
        news["source"], news["date"], news["time"] = c.span.text.replace("&nbsp;", " ").strip().split(" ")
        news["content"] = c.find("div", {"class": "c-summary"}).text.replace(u"&nbsp;百度快照", "").strip()
        news_list.append(news)
        #print c
    return news_list



if __name__=="__main__":
    keywords = ["姚贝娜", "春晚"]
    result = search_news(keywords=keywords)
    print len(result)
    for ret in result:
        print ret["title"], " ", ret["source"], ret["time"], ret["date"]
        print "    ", ret["content"], "\n"
#    content = """<li class="result" id="10">
#    <h3 class="c-title"><a href="http://news.zynews.com/2014-02/13/content_9159505.htm" data-click="{
#      'f0':'77A717EA',
#      'f1':'9F53F1E4',
#      'f2':'4CA6DE6E',
#      'f3':'54E5243F',
#      't':'1392446536'
#      }" target="_blank"><em>春晚</em>被毙小品成“主菜”</a>
#      </h3>
#      <span class="c-author">&nbsp;中原网&nbsp;2014-02-12 16:48:39</span>
#      <div class="c-summary">冯小刚已于几天前带领张国立、<em>姚贝娜</em>等“冯家班”艺人,早早离开了<em>春晚</em>导演组。   魔术换人 傅琰东又来了   近日,记者从参加央视元宵晚会的演员中了解到,蔡明...&nbsp;
#      <a href="http://cache.baidu.com/c?m=9f65cb4a8c8507ed4fece763104a802358438014749c8c423a958448e435061e5a66e1b821351072d1c5616400b21801b6b6612e711427c390cb8f41dab9953f2fff7d722f08c31c528516b8bd4632b224875b99b869e4ad803484afa2c4ae5244bb59127af1e7fb5c1764b97881622694d0&amp;p=9d769a47808511a05eb7882559&amp;newp=8f7dc91dca9f12a05abd9b785f53d8304503c5222396877879&amp;user=baidu&amp;fm=sc&amp;query=%D2%A6%B1%B4%C4%C8+%B4%BA%CD%ED&amp;qid=c589015c00c029a7&amp;p1=10" data-click="{'fm':'sc'}" target="_blank" class="c-cache">百度快照
#      </a>
#      </div></li>
#"""
#    soup = BeautifulSoup(content)
#
#    print soup.li.find("div", {"class": "c-summary"}).next
