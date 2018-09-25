# -*-coding:utf-8 -*-
__author__ = 'Cenergy'
__date__ = '6/8/18 下午2:45'

from django.conf.urls import url, include
from api import views

from rest_framework.routers import DefaultRouter
router = DefaultRouter()

#router.register(r'goods', GoodsListViewSet, base_name='goods')

urlpatterns = [
    url(r'v1/goods/$', views.SnippetList.as_view(), name="goods"),
    url(r'', include(router.urls)),
]
