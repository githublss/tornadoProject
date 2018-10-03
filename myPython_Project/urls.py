#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from handlers import Passport, VerifyCode, Profile,House
from handlers.BaseHandler import StaticFileBaseHandler
urls = [
    # (r"/", Passport.IndexHandler),
    (r"/api/piccode", VerifyCode.PicCodeHandler),
    (r"/api/smscode", VerifyCode.SMSCodeHandler),
    (r"/api/register", Passport.RegisterHandler),
    (r"/api/login",Passport.LoginHandler),
    (r"/api/check_login", Passport.CheckLoginHandler),
    (r"/api/profile/avatar", Profile.AvatarHandler),
    (r"/api/profile", Profile.ProfileHandler),
    (r"/api/house/area", House.AreaInfoHandler),
    # (r'^/api/house/info$', House.HouseInfoHandler), # 上传房屋的基本信息
    (r'^/api/house/my$', House.MyHousesHandler), # 查询用户发布的房源
    (r'^/api/house/index$', House.IndexHandler), # 首页
    (r"/(.*)",StaticFileBaseHandler,dict(path=os.path.join(os.path.dirname(__file__),"html"),
                                         default_filename="index.html")),  # 此处的设置不是很明白---------
]