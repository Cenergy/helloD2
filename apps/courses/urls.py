# -*-coding:utf-8 -*-
__author__ = 'Cenergy'
__date__ = '6/8/18 下午4:49'

from django.conf.urls import url, include
from courses import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^img2excel/$', csrf_exempt(views.ImagetoExcel.as_view()), name="img2excel"),
    url(r'^blog/', views.blog, name="blog"),
    url('^', views.OrgView.as_view(), name="courses"),
]
