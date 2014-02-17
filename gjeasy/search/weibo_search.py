#coding: utf8

#__author__="hhl"
from datetime import datetime

import urllib
import urllib2
import cookielib
import mechanize
from BeautifulSoup import BeautifulSoup

WEIBO_BASE_URL = "http://s.weibo.com/weibo/"

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

def search_weibo(keyword):
    if not keyword:
        return

    new_weibo = {}
    encode_words = urllib.quote(keyword.encode("utf-8"))
    url = "%s%s" % (WEIBO_BASE_URL, encode_words)

    result = br.open(url).read()

    soup = BeautifulSoup(result)
    new_weibo["addr"] = soup.find("p", {"class": "person_addr"}).a.string
    new_weibo["content"] = soup.findAll("div", {"class": "person_newwb"})[0].text
    year = "%s-" % datetime.now().year
    new_weibo["time"] = year + soup.find("div", {"class": "person_newwb"}).p.findAll("a")[-1].text\
        .strip("(").strip(")").replace(u"月", "-").replace(u"日", "").strip(" ") + ":00"

    return new_weibo


if __name__=="__main__":
    keyword = "姚贝娜"
    print search_weibo(keyword=keyword)
    html = """
<p class="person_addr">
<span class="female m_icon"></span>
<span>北京</span>
<a href="http://weibo.com/bellamusic" target="_blank" class="wb_url" suda-data="key=tblog_search_v4.1&amp;value=direct_user_url_nologin:_nologin">http://weibo.com/bellamusic</a>
</p>
<p class="person_card">内地知名女歌手 中国好声音学员姚贝娜</p> <p class="person_num">
<span>关注<a href="http://weibo.com/bellamusic" target="_blank" suda-data="key=tblog_search_v4.1&amp;value=direct_user_num_nologin:1_02_1268252377_nologin">597</a></span>
<em class="W_vline">|</em>
<span>粉丝<a href="http://weibo.com/bellamusic" target="_blank" suda-data="key=tblog_search_v4.1&amp;value=direct_user_num_nologin:1_02_1268252377_nologin">334万</a></span>
<em class="W_vline">|</em>
<span>微博<a href="http://weibo.com/bellamusic" target="_blank" suda-data="key=tblog_search_v4.1&amp;value=direct_user_num_nologin:1_02_1268252377_nologin">807</a></span>
</p>
</div>
</div>
<div class="person_newwb">
<p>
<a href="http://weibo.com/1268252377/AwyIUm0xC" target="_blank" suda-data="key=tblog_search_v4.1&amp;value=direct_user_new_weibo_nologin">最新微博</a>：虽然这次未能加入元宵晚会的表演 但我知道你们一直为了我在努力着!我亲爱的大宝贝们 无论遇到什么样的困难 也不会阻止我前行的脚步 把它视作上天对我们的考验 我向往的还是那样一个充满力量与阳光的舞台 一直没有改变 我知道 你们一直在 爱你们<img src="http://img.t.sinajs.cn/t3/style/images/common/face/emimage/ee8196.png" width="20px" height="20px" />快乐前行 无怨无悔!<a href="http://weibo.com/1268252377/AwyIUm0xC" target="_blank" suda-data="key=tblog_search_v4.1&amp;value=direct_user_new_pic_nologin"><span class="feedico_image" title=""></span></a> <a href="http://weibo.com/1268252377/AwyIUm0xC" target="_blank" suda-data="key=tblog_search_v4.1&amp;value=direct_user_new_time_nologin">(2月13日 19:39)</a> </p>
</div>

    """
    #soup = BeautifulSoup(html)
    #print soup.find("p", {"class": "person_addr"}).a.string
    #print soup.findAll("p", {"class": "person_addr"})[0].text
    #print soup.findAll("div", {"class": "person_newwb"})[0].text
    #print soup.find("div", {"class": "person_newwb"}).p.findAll("a")[-1].text.strip(" ").strip("(").strip(")")
    #str = u"2月13日 19:39"
    #print str.replace(u"月", "-").replace(u"日", "")
