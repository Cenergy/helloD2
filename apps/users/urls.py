# -*-coding:utf-8 -*-
__author__ = 'Cenergy'
__date__ = '6/8/18 下午2:45'

from django.conf.urls import url, include
from django.urls import path
from django.views.generic import TemplateView
import users.views
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
    url('jwt/activate/$', csrf_exempt(views.JwtActivatePwdView.as_view()), name="activate"),
    url('jwt/reset/$', csrf_exempt(views.JwtResetPwdView.as_view()), name="reset"),
    url('deleteface/$', csrf_exempt(views.DeleteFaceView.as_view()), name="deleteface"),
    url('facelink/$', csrf_exempt(views.FaceLink.as_view()), name="facelink"),
    url('regface/$', csrf_exempt(views.RegImage.as_view()), name="regface"),
    url('logout/$', views.LogoutView.as_view(), name="logout"),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^user_suggest/$', csrf_exempt(views.UserSuggestion.as_view()),
        name="user_suggest"),
    url(r'^get_voices/$', views.get_voices),
    url(r'^BANAJAX/$', views.BANAJAX),
    url(r'^$', views.VuePageView.as_view(), name="vue"),
]
