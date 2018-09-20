# -*-coding:utf-8 -*-
__author__ = 'Cenergy'
__date__ = '14/9/18 下午5:07'

from django.conf.urls import url, include
from django.views.generic import TemplateView
from wechat.views import weixin_main
from sources.views import QueryWechat, WechatTalk, SourcesUpload, ImgtoWords

from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^wxtalk/', WechatTalk.as_view(), name="talk_wechat"),
    url(r'^upload/', csrf_exempt(SourcesUpload.as_view()), name="upload"),
    url(r'^img2words/', csrf_exempt(ImgtoWords.as_view()), name="img2words"),
    url(r'^query_wechat/$', csrf_exempt(QueryWechat.as_view()), name="query_wechat"),
    url('^', weixin_main, name="wechat"),
]
