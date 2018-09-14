# -*-coding:utf-8 -*-
__author__ = 'Cenergy'
__date__ = '14/9/18 下午5:31'

import xadmin
from xadmin import  views
from  .models import SourcesCore



class SourcesCoreAdmin(object):
    list_display=['sourcename','sourceurl','code','sourcedesc','send_time']
    search_fields = ['id','sourcename','sourceurl','code','sourcedesc','send_time']
    list_filter=['id','sourcename','sourceurl','code','sourcedesc','send_time']
    exclude = ['id']  # 隐藏字段
xadmin.site.register(SourcesCore,SourcesCoreAdmin)
