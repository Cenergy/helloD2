from django.test import TestCase

# Create your tests here.

#coding=utf-8
import requests
import base64
import json
import requests

# 图片地址
# img_url = "http://imglf0.nosdn.127.net/img/RWppUi92Wk1nQzFtTUtCdUdwY2Vkd1pPekVqZ1RhT0VRZVJkeFhRanc0d2Vwa2dVUmUrR25RPT0.jpg?imageView&thumbnail=500x0&quality=96&stripmeta=0&type=jpg"
# img = requests.get(picurl)
# with open('test.jpg', 'ab') as f:
#     f.write(img.content)

# # """ 你的 APPID AK SK """
# APP_ID = '11800206'
# API_KEY = 'sAy8l7GrgGMBfesVoPkYtr0m'
# SECRET_KEY = 'Ex4Yitab1ZTq8y3FykTpa3kbGvpfUvjV'

import urllib, sys
import ssl

# headers = {"Content-Type":"application/x-www-form-urlencoded"}
#
# with open(r"hello.jpg",'rb') as f:
#     data = f.read()
# b64pic = base64.b64encode(data)
# data={"image":b64pic}
#
# # client_id 为官网获取的AK， client_secret 为官网获取的SK
# host = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?grant_type=client_credentials&client_id=sAy8l7GrgGMBfesVoPkYtr0m&client_secret=Ex4Yitab1ZTq8y3FykTpa3kbGvpfUvjV"
# a=requests.post(host,headers=headers,data=data)
# print(a.text)

# -*- coding: UTF-8 -*-

# from aip import AipOcr
#
#
# # 定义常量
# # APP_ID = '14238582'
# # API_KEY = 'sAy8l7GrgGMBfesVoPkYtr0m'
# # SECRET_KEY = 'Ex4Yitab1ZTq8y3FykTpa3kbGvpfUvjV'
#
# # 初始化文字识别分类器
# # aipOcr=AipOcr(APP_ID, API_KEY, SECRET_KEY)
#
# # 读取图片
#
# def get_file_content(filePath):
#     with open(filePath, 'rb') as fp:
#         return fp.read()
#
# # 定义参数变量
# options = {
#     'detect_direction': 'true',
#     'language_type': 'CHN_ENG',
# }
#
# # result = aipOcr.webImage(get_file_content('hello.jpg'),options)
#
#
# """ 调用表格识别结果 """
# # 初始化文字识别分类器
# aipOcr=AipOcr('14238582', 'GLfcrhzmAepajd0WpEWTnpCV', 'gdAsgciejTyEtF6vyUPpwVeedSeSDTHu')
# image = get_file_content('hello.jpg')
# hhh=aipOcr.tableRecognitionAsync(image)
# print(hhh)
# import datetime
# """ 带参数调用表格识别结果 """
# picUrl="error"
# # options['result_type']='json'
# starttime = datetime.datetime.now()
# while True:
#
#     try:
#         requestId = hhh["result"][0]["request_id"]
#         aaa = aipOcr.getTableRecognitionResult(requestId, options)
#         picUrl=aaa["result"]["result_data"]
#         if  picUrl!='':
#             break
#     except:
#         pass
#     endtime = datetime.datetime.now()
#     if (endtime - starttime).seconds>20:
#         picUrl = "error"
#         break
# print(picUrl)


# wx5e81f80b5c18df38
# 135d7bf90a542cc71b46e99bba133e79
#coding=utf-8
import requests
import base64
import json
with open(r"hhh.jpg",'rb') as f:
    data = f.read()


import datetime

a=datetime.datetime.now()
b=datetime.timedelta(days=1,hours=0, minutes=0, seconds=0)
c=datetime.timedelta(days=0,hours=22, minutes=0, seconds=0)
today = datetime.date.today()
yestoday = today - datetime.timedelta(days=1)
tomorrow = today + datetime.timedelta(days=1)
print(yestoday,today,tomorrow)



