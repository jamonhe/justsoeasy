#coding: utf8

import HTMLParser
import urlparse
import urllib
import urllib2
import cookielib
import string
import re
import os

def auto_login_hi(request_url, commit_url, username, password):
    #设置cookie
    cookie = cookielib.CookieJar()
    cj = urllib2.HTTPCookieProcessor(cookie)
    #设置登录参数
    postdata = urllib.urlencode({'username': username,'password': password})
    #生成请求
    request = urllib2.Request(commit_url, postdata)
    #登录百度
    opener = urllib2.build_opener(cj)
    f = opener.open(request)
    print f
    #打开百度HI空间页面
    hi_html = opener.open(request_url)
    return hi_html

if __name__=='__main__':
    username  = '13476261942'
    password = 'qiongo16739'
    request_url = 'http://music.baidu.com/search?key=%E5%BF%83%E7%81%AB'#例如：url='http://hi.baidu.com/cdkey51'
    commit_url = "https://passport.baidu.com/v2/api/?login"
    song_url = "http://play.baidu.com/?__m=mboxCtrl.playSong&__a=88352776&__o=/song/88352776||playBtn&fr=-1||-1#loaded"

    h = auto_login_hi(song_url, commit_url, username, password)
    file_path = "e:/test.html"
    fp = open(file_path, "w")
    content = h.read()
    fp.write(content)
    print content#h里面的内容便是登录后的页面内容