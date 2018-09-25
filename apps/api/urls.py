# -*-coding:utf-8 -*-
__author__ = 'Cenergy'
__date__ = '6/8/18 下午2:45'

from django.conf.urls import url, include
from api import views

urlpatterns = [
    url(r'v1/goods/$', views.SnippetList.as_view(), name="goods"),
]
