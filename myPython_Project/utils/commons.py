#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by lss on 2018/9/24

import functools
from utils.response_code import RET
def required_login(fun):
    # 保证被装饰的函数对像的__name__不变
    @functools.wraps(fun)
    def wrapper(request_handler_obj, *args, **kwargs):
        if not request_handler_obj.get_current_user():
            request_handler_obj.write(dict(errcode=RET.SESSIONERR, errmsg="用户未登陆"))
        else:
            fun(request_handler_obj, *args, **kwargs)
    return wrapper

if __name__ == '__main__':
    pass