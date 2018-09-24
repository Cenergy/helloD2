# -*-coding:utf-8 -*-
__author__ = 'Cenergy'
__date__ = '24/9/18 上午11:13'


from django.utils.deprecation import MiddlewareMixin

# django 2.0 之后中间键必须继承 django.utils.deprecation.MiddlewareMixin

class RecordUrlMiddleware(MiddlewareMixin):
    exclude_url = ["/login/"]

    def process_view(self, request, view_func, *args, **kwargs):
        if request.path not in RecordUrlMiddleware.exclude_url and request.is_ajax() is False:
            url = request.get_full_path()
            request.session["pre_url_path"] = url