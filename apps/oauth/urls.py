# -*-coding:utf-8 -*-
__author__ = 'Cenergy'
__date__ = '14/9/18 下午5:07'

from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from oauth import views

# ais 的相关路由
urlpatterns = [
    url(r'^github/', csrf_exempt(views.SourcesUpload.as_view()), name="github")
]
