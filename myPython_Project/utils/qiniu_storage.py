#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by lss on 2018/9/22
import qiniu.config
import logging

from qiniu import Auth, put_data, etag, urlsafe_base64_encode

# 需要填写你的 Access Key 和 Secret Key
access_key = 'jAD3oFvd0qDuhkKUFnpjN9yWiBOcJvpcp4Wp4cnZ'
secret_key = 'BVue9oWiuWOrNrDd1OkGQGH1ugbJWxjTR7j_TSgy'

def storage(file_data):
    try:
        # 构建鉴权对象
        q = Auth(access_key, secret_key)

        # 要上传的空间
        bucket_name = 'ourhome'

        # 上传到七牛后保存的文件名
        # key = 'my-python-logo.png';

        # 生成上传 Token，可以指定过期时间等
        token = q.upload_token(bucket_name)

        #要上传文件的本地路径
        # localfile = './sync/bbb.jpg'
        # ret, info = put_file(token, key, localfile)
        ret, info = put_data(token, None, file_data)    # ret中的key是七牛给文件起的名字
    except Exception as e:
        logging.error(e)
        raise e
    print(ret)
    print("*"*16)
    print(info)
    # assert ret['key'] == key
    # assert ret['hash'] == etag(localfile)
    print(type(info))
    print(info.status_code)
    if 200 == info.status_code:
        return ret["key"]
    else:
        raise Exception("上传失败")


if __name__ == "__main__":
    file_name = raw_input("input file name")
    with open(file_name, "rb") as file:
        file_data = file.read()
        name=storage(file_data)
    print name