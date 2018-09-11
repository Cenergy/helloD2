# -*-coding:utf-8 -*-
__author__ = 'Cenergy'
__date__ = '6/8/18 下午2:45'

from django.conf.urls import url, include
from django.views.generic import TemplateView
import users.views
import xadmin
from users import views

urlpatterns = [
    url('login/$', views.LoginView.as_view(), name="login"),
    url('test/$', views.test, name="test"),
    url('map/$', views.map),
    url('logout/$', views.LogoutView.as_view(), name="logout"),
    url('register/$', views.RegisterView.as_view(), name="register"),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', views.ActiveUserView.as_view(), name="user_active"),
    url(r'^reset/(?P<reset_code>.*)/$', views.ResetPwdView.as_view(), name="reset_pwd"),
    url(r'^forget/$', views.ForgetPwdView.as_view(), name="forget_pwd"),
    url(r'^modify_pwd/$', views.ModifyPwdView.as_view(), name="modify_pwd"),
    url(r'^user_info/$', views.UserinfoView.as_view(), name="user_info"),
    url(r'^get_voices/$', views.get_voices),
    url(r'^BANAJAX/$', views.BANAJAX),
    url('^$', views.IndexView.as_view(), name="index"),
]
