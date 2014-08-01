#coding=utf8
import time

import tornado.httpserver
import tornado.ioloop
import tornado.web
from gjeasy.logger import logger
from gjeasy.controls.get_msg import get_msg
from gjeasy.controls.send_msg import gen_news_str, gen_weibo_str

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        word = self.get_argument('word', '').split(" ")
        start_time = time.time()
        result = get_msg(keyword=word)
        end_time = time.time()
        result = gen_news_str(result["news"])# + gen_weibo_str(result["weibo"])

        logger.debug("found result: %s" % result)
        logger.debug("this search took %s seconds" % (end_time-start_time))
        self.write(result.replace("\n", "<br>").replace(" ", "&nbsp;"))

application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8880)
    tornado.ioloop.IOLoop.instance().start()