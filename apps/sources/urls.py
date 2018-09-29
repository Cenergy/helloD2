# -*-coding:utf-8 -*-
__author__ = 'Cenergy'
__date__ = '14/9/18 下午5:07'

from django.conf.urls import url, include
from django.views.generic import TemplateView
from wechat.views import weixin_main
from sources.views import QueryWechat, WechatTalk, SourcesUpload, ImgtoWords, img2wordRes, ImgtoExcel, \
    excel_download, sourceExcel,sourceList
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from sources import views

urlpatterns = [
    url('img2wordRes/$', img2wordRes, name="img2wordRes"),
    url('sourceExcel/$', sourceExcel, name="sourceExcel"),
    url('excel_download/$', excel_download, name="excel_download"),
    url(r'^wxtalk/', WechatTalk.as_view(), name="talk_wechat"),
    url(r'^upload/', csrf_exempt(SourcesUpload.as_view()), name="upload"),
    url(r'^img2words/', csrf_exempt(ImgtoWords.as_view()), name="img2words"),
    url(r'^img2excel/', csrf_exempt(ImgtoExcel.as_view()), name="img2excel"),
    url(r'^query_wechat/$', csrf_exempt(QueryWechat.as_view()), name="query_wechat"),
    url('^', sourceList, name="sources"),
]
