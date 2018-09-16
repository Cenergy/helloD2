# -*-coding:utf-8 -*-
__author__ = 'Cenergy'
__date__ = '14/9/18 下午5:07'

from django.conf.urls import url, include
from django.views.generic import TemplateView
from wechat.views import weixin_main
from sources.views import QueryWechat, WechatTalk

from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^wxtalk/', WechatTalk.as_view(), name="talk_wechat"),
    url(r'^query_wechat/$', csrf_exempt(QueryWechat.as_view()), name="query_wechat"),
    url('^', weixin_main, name="wechat"),
]
