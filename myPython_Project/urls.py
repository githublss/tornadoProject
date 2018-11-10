#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from handlers import Passport, VerifyCode, Profile, House, Orders
from handlers.BaseHandler import StaticFileBaseHandler
urls = [
    # (r"/", Passport.IndexHandler),
    (r"/api/piccode", VerifyCode.PicCodeHandler),   # 图片验证
    (r"/api/smscode", VerifyCode.SMSCodeHandler),   # 短信验证
    (r"/api/register", Passport.RegisterHandler),   # 登陆页面
    (r"/api/login",Passport.LoginHandler),          # 注册页面
    (r"/api/logout", Passport.LogoutHandler),       # 退出
    (r"/api/check_login", Passport.CheckLoginHandler),  # 检测是否登陆
    (r"/api/profile/avatar", Profile.AvatarHandler),    # 头像上传
    (r"/api/profile/name$", Profile.NameHandler),       # 修改用户名
    (r"/api/profile/auth", Profile.AuthHandler),    # 实名认证
    (r"^/api/profile", Profile.ProfileHandler),     # 个人主页获取个人信息
    (r"^/api/house/area", House.AreaInfoHandler),    # 列出区域信息
    (r'^/api/house/image$', House.HouseImageHandler),  # 上传房屋图片
    (r"^/api/house/list", House.HouseListHandler),   # 列出房屋信息
    (r'^/api/house/list2$', House.HouseListRedisHandler), # 房屋过滤列表数据
    (r'^/api/house/info$', House.HouseInfoHandler), # 上传，查看房屋的基本信息
    (r'^/api/house/my$', House.MyHousesHandler), # 查询用户发布的房源
    (r'^/api/house/index$', House.IndexHandler), # 首页

    (r'^/api/order$', Orders.OrderHandler), # 下单
    (r'^/api/order/my$', Orders.MyOrdersHandler), # 我的订单，作为房客和房东同时适用
    (r'^/api/order/accept$', Orders.AcceptOrderHandler), # 接单
    (r'^/api/order/reject$', Orders.RejectOrderHandler), # 拒单
    (r'^/api/order/comment$', Orders.OrderCommentHandler),
    (r"/(.*)",StaticFileBaseHandler,dict(path=os.path.join(os.path.dirname(__file__),"html"),
                                         default_filename="index.html")),  # 此处的设置不是很明白---------
]