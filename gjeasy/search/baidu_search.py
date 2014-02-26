#coding: utf8
import traceback

__author__="hhl"

import urllib
import urllib2
import cookielib
import mechanize
from BeautifulSoup import BeautifulSoup
from datetime import datetime
from gjeasy.logger import logger
import time

BAIDU_BASE_URL = {
    "news": "http://news.baidu.com/ns?",
}
br = mechanize.Browser()

def search_news(keywords=[], num=5):
    if not keywords:
        return
    #print keywords

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
        try:
            news = {}
            news["title"] = c.a.text.strip()
            news["addr"] = c.a.get("href")
            news["image"] = [img.get("src") for img in c.findAll("img")]

            temp = c.span.text.replace("&nbsp;", " ").strip().split(" ", 1)
            if len(temp) != 2:
                continue
            news["source"], news["time"] = temp
            news["content"] = c.find("div", {"class": "c-summary"}).text\
                .replace(u"&nbsp;百度快照", "").strip()
            news_list.append(news)
        except AttributeError, e:
            logger.warning(e)
            continue
        except Exception, e:
            logger.error(traceback.format_exc(e))
            continue

    return news_list



if __name__=="__main__":
    keywords = [u"姚贝娜"]
    result = search_news(keywords=keywords)

    print len(result)
    for ret in result:
        print ret["title"], " ", ret["source"]
        print ret["time"], ret["addr"], ret["image"]
        print "    ", ret["content"], "\n\n"
    #
    ##str = "2014-02-13 10:33:00"
    #
    str = """
    <li class="result" id="1">
	<h3 class="c-title">
		<a href="http://www.dqdaily.com/shishi/2014-02/26/content_1895280.htm"
		data-click="{
		'f0':'77A717EA',
		'f1':'9F63F1E4',
		'f2':'4CA6DE6E',
		'f3':'54E5343F',
		't':'1393420120'
		}" target="_blank">
			网传刘欢改编《卷珠帘》是为
			<em>
				姚贝娜
			</em>
		</a>
	</h3>
	<span class="c-author">
		&nbsp;大庆网&nbsp;2014-02-26 16:07:00
	</span>
	<div class="c-summary">
		<a class="c_photo" href="http://www.dqdaily.com/shishi/2014-02/26/content_1895280.htm"
		target="_blank">
			<img src="http://t11.baidu.com/it/u=1474164847,2237662702&amp;fm=55" alt=""
			/>
		</a>
		传刘欢改编《卷珠帘》是为
		<em>
			姚贝娜
		</em>
		网友呐喊:还我小清新 上周《中国好歌曲》刘欢战队主打之争刚刚结束,立即在网上引起一场轩然大波,不少网友开始吐槽刘欢对这8...&nbsp;
		<a href="http://cache.baidu.com/c?m=9d78d513d9d437af4f9e90690c66c0161a43f0652bd6a0020ed2843999701c011969b9fd61600705a0d8612244ea5e5c9da6752464587efc8cc8ff1b80e48f6975d3666e2b01864311d50eafbd4425dc209447b8f245a1edac7484a9a6d0d55f54ca59076d8087d11c5f&amp;p=c672cb1494904ead08e2917c154b&amp;newp=b46cc216d9c118e808e2917c1e4f92694f08d7267dc8914212d19111d4&amp;user=baidu&amp;fm=sc&amp;query=%D2%A6%B1%B4%C4%C8&amp;qid=9db72c1e004d5e67&amp;p1=1"
		data-click="{'fm':'sc'}" target="_blank" class="c-cache">
			百度快照
		</a>
	</div>
</li>"""
    import requests
    url = "http://115.29.142.18:8880/?word=%s" % (urllib.quote(u"姚贝娜".encode("utf-8")))
    requests.get(url)
