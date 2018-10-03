#!/usr/bin/env python
# -*- coding:utf-8 -*-
from tornado.web import RequestHandler,StaticFileHandler
import json
from utils.session import Session
class BaseHandler(RequestHandler):
    """自定义基类"""

    @property   #成员方法作为属性对待------------------
    def db(self):
        return self.application.db

    @property   # 这里装饰器的作用有遗忘，------------
    def redis(self):
        return self.application.redis

    def prepare(self):      # 调用的时间是------------
        self.xsrf_token
        """预解析json数据"""
        if self.request.headers.get("Content-Type","").startswith("application/json"):
            self.json_args = json.loads(self.request.body)
        else:
            self.json_args = {}

    def set_default_headers(self):
        pass

    # def write_error(self, status_code, **kwargs):
    #     pass

    def initialize(self):
        pass

    def on_finish(self):
        pass
    def get_current_user(self):
        """判断用户是否登陆"""
        self.session = Session(self)
        self.session.sava()
        return self.session.data

class StaticFileBaseHandler(StaticFileHandler):
    # 自定义静态文件处理类，当用户访问html页面时给用户设置_xsrf的cookie
    def __init__(self,*args,**kwargs):
        super(StaticFileHandler,self).__init__(*args, **kwargs)
        self.xsrf_token
