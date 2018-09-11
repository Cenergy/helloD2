#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import urllib.parse
import urllib.request
import json
import hashlib
import base64
import os.path as path

# AUDIO_PATH = path.abspath('.')

def main(path):
    f = open(path, 'rb')
    file_content = f.read()
    base64_audio = base64.b64encode(file_content)
    body = urllib.parse.urlencode({'audio': base64_audio})

    url = 'http://api.xfyun.cn/v1/service/v1/iat'
    api_key = 'd0f986393d35c8db5940708ba9788506'
    param = {"engine_type": "sms16k", "aue": "raw"}

    x_appid = '5b03be76'
    x_param = base64.b64encode(json.dumps(param).replace(' ', '').encode('utf-8'))
    x_time = int(int(round(time.time() * 1000)) / 1000)
    x_checksum_content = api_key + str(x_time) + str(x_param,'utf-8')
    x_checksum = hashlib.md5(x_checksum_content.encode('utf-8')).hexdigest()
    x_header = {'X-Appid': x_appid,
                'X-CurTime': x_time,
                'X-Param': x_param,
                'X-CheckSum': x_checksum}
    req = urllib.request.Request(url=url, data=body.encode('utf-8'), headers = x_header, method = 'POST')
    result = urllib.request.urlopen(req)
    result = result.read().decode('utf-8')
    print(result)
    return result

if __name__ == '__main__':
    main('test.wav')

