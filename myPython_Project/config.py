#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

# Application配置参数
settings = dict(
    static_path=os.path.join(os.path.dirname(__file__),'static'),
    cookie_secret='Vu+hq/vZQf+aL0y+TslwTa9a0ZdD1EX2mTRnukDx3Vw=',
    xsrf_cookies=False,
    debug=True,
)

# 数据库配置参数
mysql_options = dict(
    host='127.0.0.1',
    database='ihome',
    user='root',
    password=''
)

#Redis配置参数
redis_options = dict(
    host='127.0.0.1',
    port=6379
)

#日志配置
log_path = os.path.join(os.path.dirname(__file__),'logs/log')
log_level = 'debug'

# 密码加密密钥
passwd_hash_key = "nlgCjaTXQX2jpupQFQLoQo5N4OkEmkeHsHD9+BBx2WQ="