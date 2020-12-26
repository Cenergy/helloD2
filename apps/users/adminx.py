# -*-coding:utf-8 -*-
__author__ = 'Cenergy'
__date__ = '3/8/18 下午3:42'

import xadmin
from xadmin import views
from .models import EmailVerifyRecord, Banner, Suggestion


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'type_code', 'send_time']
    search_fields = ['code', 'email', 'type_code']
    list_filter = ['code', 'email', 'type_code', 'send_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)


class SuggestionAdmind(object):
    readonly_fields = ['suggest_content']
    list_display = ['email', 'suggest_name', 'suggest_content', 'add_time']
    search_fields = ['suggest_name', 'suggest_content', 'email', 'add_time']
    list_filter = ['suggest_name', 'suggest_content', 'email', 'add_time']
    style_fields = {'reply_content': "ueditor"}


xadmin.site.register(Suggestion, SuggestionAdmind)


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSetting(object):
    site_title = "HelloWorld"
    site_footer = "Helen"
    menu_style = "accordion"


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)
