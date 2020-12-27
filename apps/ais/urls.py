# -*-coding:utf-8 -*-
__author__ = 'Cenergy'
__date__ = '14/9/18 下午5:07'

from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from ais import views

# ais 的相关路由
urlpatterns = [
    url(r'^upload/', csrf_exempt(views.SourcesUpload.as_view()), name="upload"),
    url(r'^img2words/', csrf_exempt(views.ImgtoWords.as_view()), name="img2words"),
    url(r'^img2excel/', csrf_exempt(views.ImgtoExcel.as_view()), name="img2excel"),
    url(r'^imgupload/', csrf_exempt(views.ImageUpload.as_view()), name="imgupload"),
    url(r'^poibyname/', csrf_exempt(views.POIbyName.as_view()), name="imgupload"),
    url(r'^poibyregion/', csrf_exempt(views.POIbyRegion.as_view()), name="imgupload"),
]
