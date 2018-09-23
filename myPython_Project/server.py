#!/usr/bin/env python
# -*- coding:utf-8 -*-
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
import config
import torndb
import redis

from tornado.options import options,define
from tornado.web import RequestHandler
from urls import urls
define('port', default=8002, type=int, help='run server on the given port')

class Application(tornado.web.Application):
    def __init__(self, *args, **kwargs):
        super(Application,self).__init__(*args, **kwargs)   #这里的写法有遗忘++++
        self.db = torndb.Connection(**config.mysql_options)    # 直接进行字典解包，这里进行了代码的抽离
        self.redis = redis.StrictRedis(**config.redis_options)

# class IndexHandler(RequestHandler):
#     def get(self):
#         self.write('hello itcast')

def main():
    options.log_file_prefix = config.log_path
    options.logging=config.log_level
    tornado.options.parse_command_line()    # 作用是
    app = Application(
        urls,
        **config.settings
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port, "")
    # http_server.bind(8001)    # 将服务器绑定到8000端口
    # http_server.start(0)  #指定开启进程的数量
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()