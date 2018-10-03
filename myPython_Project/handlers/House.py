#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by lss on 2018/9/26
from handlers.BaseHandler import BaseHandler
from utils.response_code import RET
import constants
import logging
import json
from utils.commons import required_login
class AreaInfoHandler(BaseHandler):
    """提供区域信息"""
    def get(self):
        # 查询Redis数据库
        try:
            ret = self.redis.get("area_info")
        except Exception as e:
            logging.error(e)
            ret = None
        if ret:
            logging.info("hit redis:area_info")
            resp = '{"errcode":%s,"errmsg":"OK","data":%s}' % (RET.OK, ret)
            return self.write(resp)
        # Redis数据库中没有数据再在MySQL中进行查询
        sql = "select ai_area_id,ai_name from ih_area_info;"
        try:
            ret = self.db.query(sql)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg="数据库查询失败"))
        if not ret:
            return self.write(dict(errcode=RET.NODATA, errmsg="没有数据"))

        # 保存查询好的数据
        data = []
        for row in ret:
            d={
                "area_id":row.get("ai_area_id"),
                "name": row.get("ai_name")
            }
            data.append(d)
        # 在返回给用户信息之前保存一份副本在redis中
        json_data = json.dumps(data)
        try:
            self.redis.setex("area_info",constants.REDIS_AREA_INFO_EXPIRES_SECONDES,json_data)
        except Exception as e:
            logging.error(e)
        self.write(dict(errcode=RET.OK,errmsg="OK",data=data))

class MyHousesHandler(BaseHandler):
    """用户房屋信息获取"""
    @required_login
    def get(self):
        user_id = self.session.data["user_id"]
        try:
            sql = "select a.hi_house_id,a.hi_title,a.hi_price,a.hi_ctime,b.ai_name,a.hi_index_image_url " \
                  "from ih_house_info a inner join ih_area_info b on a.hi_area_id=b.ai_area_id where a.hi_user_id=%s;"
            ret = self.db.query(sql, user_id)
        except Exception as e:
            logging.error(e)
            return self.write({"errcode":RET.DBERR, "errmsg":"get data erro"})
        houses = []
        if ret:
            for l in ret:
                house = {
                    "house_id":l["hi_house_id"],
                    "title":l["hi_title"],
                    "price":l["hi_price"],
                    "ctime":l["hi_ctime"].strftime("%Y-%m-%d"), # 将返回的Datatime类型格式化为字符串
                    "area_name":l["ai_name"],
                    "img_url":constants.QINIU_URL_PREFIX + l["hi_index_image_url"] if l["hi_index_image_url"] else ""
                }
                houses.append(house)
        self.write({"errcode":RET.OK, "errmsg":"OK", "houses":houses})

class IndexHandler(BaseHandler):
    """主页信息"""

    def get(self):
        try:
            ret = self.redis.get("home_page_data")
        except Exception as e:
            logging.error(e)
            ret = None
        if ret:
            json_houses = ret
        else:
            try:
                # 查询数据库，返回房屋订单数目最多的5条数据(房屋订单通过hi_order_count来表示）
                house_ret = self.db.query(
                    "select hi_house_id,hi_title,hi_order_count,hi_index_image_url from ih_house_info " \
                    "order by hi_order_count desc limit %s;" % constants.HOME_PAGE_MAX_HOUSES)
            except Exception as e:
                logging.error(e)
                return self.write({"errcode": RET.DBERR, "errmsg": "get data error"})
            if not house_ret:
                return self.write({"errcode": RET.NODATA, "errmsg": "no data"})
            houses = []
            for l in house_ret:
                if not l["hi_index_image_url"]:
                    continue
                house = {
                    "house_id": l["hi_house_id"],
                    "title": l["hi_title"],
                    "img_url": constants.QINIU_URL_PREFIX + l["hi_index_image_url"]
                }
                houses.append(house)
            json_houses = json.dumps(houses)
            try:
                self.redis.setex("home_page_data", constants.HOME_PAGE_DATA_REDIS_EXPIRE_SECOND, json_houses)
            except Exception as e:
                logging.error(e)

        # 返回首页城区数据
        try:
            ret = self.redis.get("area_info")
        except Exception as e:
            logging.error(e)
            ret = None
        if ret:
            json_areas = ret
        else:
            try:
                area_ret = self.db.query("select ai_area_id,ai_name from ih_area_info")
            except Exception as e:
                logging.error(e)
                area_ret = None
            areas = []
            if area_ret:
                for area in area_ret:
                    areas.append(dict(area_id=area["ai_area_id"], name=area["ai_name"]))
            json_areas = json.dumps(areas)
            try:
                self.redis.setex("area_info", constants.REDIS_AREA_INFO_EXPIRES_SECONDES, json_areas)
            except Exception as e:
                logging.error(e)
        resp = '{"errcode":"0", "errmsg":"OK", "houses":%s, "areas":%s}' % (json_houses, json_areas)
        self.write(resp)