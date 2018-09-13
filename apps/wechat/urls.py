# -*-coding:utf-8 -*-
__author__ = 'Cenergy'
__date__ = '13/9/18 下午3:17'


from django.conf.urls import url, include
from django.views.generic import TemplateView
from wechat import views

urlpatterns = [
    url('^', views.weixin_main,name="wechat"),
]
