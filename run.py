#coding=utf8
import time

import tornado.httpserver
import tornado.ioloop
import tornado.web
from views.base import get_msg


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        word = self.get_argument('word', '').split(" ")
        start_time = time.time()
        result = get_msg(keywords=word)
        end_time = time.time()
        print result
        print "took %s seconds" % (end_time-start_time)
        self.write(result)

application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8880)
    tornado.ioloop.IOLoop.instance().start()