# -*-coding:utf-8 -*-
__author__ = 'Cenergy'
__date__ = '6/8/18 下午2:45'

from django.conf.urls import url, include
from django.views.generic import TemplateView
import users.views
import xadmin
from users import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^captcha/', include('captcha.urls')),
    url('^$', views.IndexView.as_view(), name="index"),
]
