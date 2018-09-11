# -*-coding:utf-8 -*-
__author__ = 'Cenergy'
__date__ = '6/8/18 下午4:49'

from django.conf.urls import url, include
from courses import views

urlpatterns = [
    url('^', views.OrgView.as_view(), name="courses"),
]
