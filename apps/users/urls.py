# -*-coding:utf-8 -*-
__author__ = 'Cenergy'
__date__ = '6/8/18 下午2:45'

from django.conf.urls import url, include
from django.urls import path
from django.views.generic import TemplateView
import users.views
import xadmin
from users import views
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    url('jwt/login/$', csrf_exempt(views.JwtLoginView.as_view()), name="jwt"),
    url('jwt/order/$', csrf_exempt(views.JwtOrderView.as_view()), name="order"),
    url('jwt/register/$', csrf_exempt(views.JwtRegisterView.as_view()), name="register"),
    url('jwt/forget/$', csrf_exempt(views.JwtForgetPwdView.as_view()), name="forget"),
    url('login1/$', views.UserLoginView.as_view(), name="login1"),
    url('register1/$', views.UserRegisterView.as_view(), name="register1"),
    url(r'^active1/(?P<active_code>.*)/$',
        views.UserActiveView.as_view(), name="user_active1"),
    url(r'^forget1/$', views.UserForgetPwdView.as_view(), name="forget_pwd1"),
    url(r'^reset1/(?P<reset_code>.*)/$',
        views.UserResetPwdView.as_view(), name="reset_pwd1"),
    url(r'^modify_pwd1/$', views.UserModifyPwdView.as_view(), name="modify_pwd1"),



    url('login/$', views.LoginView.as_view(), name="login"),
    url('face123/$', csrf_exempt(views.FaceLoginView.as_view()), name="face123"),
    url('deleteface/$', csrf_exempt(views.DeleteFaceView.as_view()), name="deleteface"),
    url('facereg/$', views.FaceRegView.as_view(), name="facereg"),
    url('test/', views.test, name="test"),
    url('map/$', views.map),
    url(r'^vue/', views.VuePageView.as_view(), name="vue"),
    url('aboutme/$', TemplateView.as_view(template_name='aboutme.html'), name="about_me"),
    url('facelink/$', csrf_exempt(views.FaceLink.as_view()), name="facelink"),
    url('regface/$', csrf_exempt(views.RegImage.as_view()), name="regface"),
    url('logout/$', views.LogoutView.as_view(), name="logout"),
    url('register/$', views.RegisterView.as_view(), name="register"),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$',
        views.ActiveUserView.as_view(), name="user_active"),
    url(r'^reset/(?P<reset_code>.*)/$',
        views.ResetPwdView.as_view(), name="reset_pwd"),
    url(r'^forget/$', views.ForgetPwdView.as_view(), name="forget_pwd"),
    url(r'^modify_pwd/$', views.ModifyPwdView.as_view(), name="modify_pwd"),
    url(r'^user_info/$', views.UserinfoView.as_view(), name="user_info"),
    url(r'^user_suggest/$', csrf_exempt(views.UserSuggestion.as_view()),
        name="user_suggest"),
    url(r'^get_voices/$', views.get_voices),
    url(r'^BANAJAX/$', views.BANAJAX),
    url('^$', views.IndexView.as_view(), name="index"),
]
