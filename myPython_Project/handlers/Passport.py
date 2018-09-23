#!/usr/bin/env python
# -*- coding:utf-8 -*-
from BaseHandler import BaseHandler
from utils.response_code import RET
from utils.session import Session
import logging
import re
import hashlib
import config

class IndexHandler(BaseHandler):
    def get(self):
        logging.debug('this is debug')
        logging.info('this is info')
        logging.warning('this is waring')
        logging.error('this is error')
        print 'this is print msg'
        self.write('hello itcast')

class RegisterHandler(BaseHandler):
    """注册"""
    def post(self):
        # 获取参数
        mobile = self.json_args.get("mobile")
        sms_code = self.json_args.get("photocode")
        password = self.json_args.get("password")

        # 参数的检验
        if not all((mobile,sms_code,password)):
            return self.write(dict(errcode=RET.PARAMERR, errmsg="参数不完整"))
        # 检测号码格式
        if not re.match(r"^1\d{10}$",mobile):
            return self.write(dict(errcode=RET.DATAERR, errmsg="手机格式错误"))

        # 可以检测密码长度
        # if len(password)<6:

        # 判断短信验证码
        if "2468" != sms_code:
            try:
                real_sms_code = self.redis.get("sms_code_%s" % mobile)
            except Exception as e:
                logging.error(e)
                return self.write(dict(errcode=RET.DBERR, errmsg="查询验证码出错"))
            # 判断验证码是否过期
            if not real_sms_code:
                return self.write(dict(errcode=RET.NODATA, errmsg="验证码过期"))

            # 判断填写验证码是否正确
            if real_sms_code != sms_code:
                return self.write(dict(errcode=RET.DATAERR, errmsg="验证码错误"))

            try:
                self.redis.delete("sms_code_%s"%mobile)
            except Exception as e:
                logging.error(e)

        # 保存数据，同时判断手机号是否存在，
        passwd = hashlib.sha256(password + config.passwd_hash_key,).hexdigest()     # 没有明白--------------
        sql = "insert into ih_user_profile(up_name, up_mobile, up_passwd) value(%(name)s, %(mobile)s, %(passed)s);"
        try:
            user_id = self.db.execute(sql,name=mobile,mobile=mobile, passwd=passwd)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DATAEXIST, errmsg="号码已经存在"))

        session = Session(self)
        session.data["user_id"] = user_id
        session.data["mobile"] = mobile
        session.data["name"] = mobile
        try:
            session.sava()
        except Exception as e:
            logging.error(e)
        self.write(dict(errcode=RET.OK, errmsg="注册成功"))

class LoginHandler(BaseHandler):
    """登陆"""
    def post(self):
        # 获取参数
        mobile = self.json_args.get("mobile")
        password = self.json_args.get("password")

        # 检查参数
        if not all((mobile,password)):
            return self.write(dict(errcode=RET.PARAMERR,errmsg="参数错误"))
        if not re.match(r"^1\d{10}$",mobile):
            return self.write(dict(errcode=RET.DATAERR, errmsg="手机号错误"))

        # 检查密码是否正确
        res = self.db.get("select up_user_id,upname,up_passwd from ih_user_profile where up_mobile=%(mobile)s",
                          mobile=mobile)
        password = hashlib.sha256(password + config.passwd_hash_key).hexdigest()
        if res and res["up_passwd"] == unicode(password):
            try:
                self.session = Session(self)
                self.session.data['user_id'] = res['up_user_id']
                self.session.data['name'] = res['up_name']
                self.session.data['mobile'] = mobile
                self.session.sava()
            except Exception as e:
                logging.error(e)
            return self.write(dict(errcode=RET.OK, errmsg="OK"))
        else:
            return self.write(dict(errcode=RET.DATAERR, errmsg="账号或密码错误！"))

class CheckLoginHandler(BaseHandler):
    """检查登陆状态"""
    def get(self):
        # get_current_user方法在基类中已实现，它的返回值是session.data（用户保存在redis中
        # 的session数据），如果为{} ，意味着用户未登录;否则，代表用户已登录
        if self.get_current_user():
            self.write({"errcode":RET.Ok, "errmsg":"true", "data":{"name":self.session.data.get("name")}})
        else:
            self.write({"errcode":RET.SESSIONERR,"errmsg":"false"})