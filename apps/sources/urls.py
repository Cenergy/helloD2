# -*-coding:utf-8 -*-
__author__ = 'Cenergy'
__date__ = '14/9/18 下午5:07'


from django.conf.urls import url, include
from django.views.generic import TemplateView
from wechat import views

urlpatterns = [
    url('^', views.weixin_main,name="wechat"),
]
