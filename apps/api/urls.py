# -*-coding:utf-8 -*-
__author__ = 'Cenergy'
__date__ = '6/8/18 下午2:45'

from django.conf.urls import url, include
from api import views

from rest_framework.routers import DefaultRouter

from api.views import SourcesCoreViewset


router = DefaultRouter()

router.register(r'v1/sources', SourcesCoreViewset, base_name='sources')

urlpatterns = [
    url(r'v1/goods/$', views.SnippetList.as_view(), name="goods"),
    url(r'v1/resources/$', views.SourcesList.as_view(), name="resources"),
    url(r'', include(router.urls)),
]
