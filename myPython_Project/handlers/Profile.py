#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by lss on 2018/9/22
import logging
import constants
from handlers.BaseHandler import BaseHandler
from utils.response_code import RET
from utils.qiniu_storage import storage
from utils.commons import required_login

class AvatarHandler(BaseHandler):
    """头像上传"""
    @required_login                                     # 使用此装饰器，而不用框架自带装饰器tornado.web.authenticated(method)的原因-----
    def post(self):
        files = self.request.files.get("avatar")        # 此处用法-------------
        if not file:
            return self.write(dict(errcode=RET.PARAMERR, errmsg="未传图片"))
        avatar = files[0]["body"]
        # 调用七牛上传图片
        try:
            file_name = storage(avatar)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.THIRDERR,errmsg="上传失败"))
        # 从session中取出用户的user_id
        user_id = self.session.daba["user_id"]
        sql = "updata ih_user_profile set up_avatar=%(avatar)s where up_user_id=%(user_id)s"
        try:
            row_count = self.db.execute_rowcoutn(sql,avatar=file_name, user_id=user_id)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DATAERR, errmsg="保存错误"))
        self.write(dict(RET.OK, errmsg="保存成功", data="%s%s" %(constants.QINIU_URL_PREFIX, file_name)))

class ProfileHandler(BaseHandler):
    """个人信息"""
    @required_login
    def get(self):
        user_id = self.session.data['user_id']
        try:
            ret = self.db.get("select up_name,up_mobile,up_avatar from ih_user_profile where up_user_id=%s",user_id)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg="get data error"))
        if ret["up_avatar"]:
            img_url = constants.QINIU_URL_PREFIX + ret["up_avatar"]
        else:
            img_url = None
        self.write(errcode=RET.OK, errmsg="OK",data={"user_id":user_id, "name":ret["up_name"], "mobile":ret["up_mobile"],"avatar":img_url})

if __name__ == '__main__':
    pass