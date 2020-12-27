# -*-coding:utf-8 -*-
__author__ = 'Cenergy'
__date__ = '17/10/18 上午11:46'

from .models import BlogType,Blog
import xadmin


class BlogTypeAdmin(object):
    list_display=['id','type_name']
    search_fields = ['id','type_name']
    list_filter=['id','type_name']
    # exclude = ['id']  # 隐藏字段
xadmin.site.register(BlogType,BlogTypeAdmin)


class BlogAdmin(object):
    list_display=['title','blog_type','content','author','source_img','created_time','last_update_time']
    search_fields = ['title','blog_type','content','author','created_time','last_update_time']
    list_filter=['title','blog_type','content','author','created_time','last_update_time']
    style_fields = {'content': "ueditor"}
    # exclude = ['id']  # 隐藏字段
xadmin.site.register(Blog,BlogAdmin)