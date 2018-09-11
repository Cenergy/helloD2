# -*-coding:utf-8 -*-
__author__ = 'Cenergy'
__date__ = '3/8/18 下午3:42'

import xadmin
from xadmin import  views
from  .models import EmailVerifyRecord,Banner

class EmailVerifyRecordAdmin(object):
    list_display=['code','email','type_code','send_time']
    search_fields = ['code', 'email', 'type_code']
    list_filter=['code', 'email', 'type_code','send_time']
xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)

class BannerAdmind(object):
    list_display=['title','image','url','index','add_time']
    search_fields = ['title','image','url','index','add_time']
    list_filter=['title','image','url','index','add_time']
xadmin.site.register(Banner,BannerAdmind)


class BaseSetting(object):
    enable_themes=True
    use_bootswatch=True
class GlobalSetting(object):
    site_title="HelloWorld"
    site_footer="Helen"
    menu_style="accordion"

xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSetting)
