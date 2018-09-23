#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by lss on 2018/9/15
import uuid
import json
import logging
from constants import SESSION_EXPIRES_SECONDS

class Session(object):
    def __init__(self, request_handler_obj):
        # 判断用户是否有了session_id
        self._request_handler = request_handler_obj
        self.session_id = request_handler_obj.get_secure_cookie("session_id")

        # 如果不存在session_id,生成session_id
        if not self.session_id:
            self.session_id = uuid.uuid4().hex
            self.data = {}
            request_handler_obj.set_secure_cookie("session_id", self.session_id)

        # 如果存在session_id,去redis中取出data
        else:
            try:
                json_data = request_handler_obj.redis.get("sess_%s",self.session_id)
            except Exception as e:
                logging.error(e)
                raise e
            if not json_data:
                self.data = {}
            else:
                self.data = json.loads(json_data)

    def sava(self):
        json_data = json.dump(self.data)
        try:
            self._request_handler.redis.setex("sess_%s"%self.session_id, SESSION_EXPIRES_SECONDS, json_data)
        except Exception as e:
            logging.error(e)
            raise e
    def clear(self):
        try:
            self._request_handler.redis.delete("sess_%s" % self.session_id)
        except Exception as e:
            logging.error(e)
        self._request_handler.clear_cookie("session_id") # 将cookie中的session_id删除