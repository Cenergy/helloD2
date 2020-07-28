# -*-coding:utf-8 -*-
__author__ = 'Cenergy'
__date__ = '6/8/18 下午2:45'

from django.conf.urls import url, include
from api import views

from rest_framework.routers import DefaultRouter

from api.views import SourcesCoreViewset
from django.views.decorators.csrf import csrf_exempt

router = DefaultRouter()

router.register(r'v1/sources', SourcesCoreViewset, basename='sources')

urlpatterns = [
    url(r'v1/goods/$', views.SnippetList.as_view(), name="goods"),
    url(r'v1/blogs/$', views.BlogListView.as_view(), name="blogs"),
    url(r'v1/blogs/(?P<blog_pk>\d+)/$',
        views.BlogDetailView.as_view(), name="blogs_detail"),
    url(r'v1/blog_types/(?P<blog_type>\d+)/$',
        views.BlogTypeView.as_view(), name="blogs_detail"),
    url(r'v1/suggestions/', csrf_exempt(views.SuggestionsView.as_view()),
        name="suggestions"),
    url(r'v1/resources/$', views.SourcesList.as_view(), name="resources"),
    url(r'v1/sources/$', views.SourcesListView.as_view(), name="sources"),
    url(r'jwt/login/$', csrf_exempt(views.JwtLoginView.as_view())),
    url(r'', include(router.urls)),
]
