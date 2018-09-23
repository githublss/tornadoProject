#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from handlers import Passport,VerifyCode
from handlers.BaseHandler import StaticFileBaseHandler
urls = [
    # (r"/", Passport.IndexHandler),
    (r"/api/piccode", VerifyCode.PicCodeHandler),
    (r"/api/smscode",VerifyCode.SMSCodeHandler),
    (r"/(.*)",StaticFileBaseHandler,dict(path=os.path.join(os.path.dirname(__file__),"html"),
                                         default_filename="index.html")),  # 此处的设置不是很明白---------
]