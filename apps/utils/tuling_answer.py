# -*-coding:utf-8 -*-
__author__ = 'Cenergy'
__date__ = '15/9/18 上午10:37'

import requests
from helloD2.settings import TURING_API_KEY

apiUrl = 'http://www.tuling123.com/openapi/api'


def get_tuling_answer(question):
    data = {
        'key': TURING_API_KEY,  # 如果这个Tuling Key不能用，那就换一个
        'info': question,  # 这是我们发出去的消息
        'userid': 'wechat-robot',  # 这里你想改什么都可以
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        # 字典的get方法在字典没有'text'值的时候会返回None而不会抛出异常
        return r.get('text')
        # 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常
        # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
    except:
        # 将会返回一个None
        return "暂时找不到答案"
