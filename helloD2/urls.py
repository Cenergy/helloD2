"""helloD URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from django.views.generic import TemplateView
import users.views, courses.views, sources.views
import xadmin
from users import views
from wechat import views
from helloD2 import settings
from django.views import static
from rest_framework.documentation import include_docs_urls
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title="我的docs")

# custom_error的路由!
handler403 = users.views.permission_denied
handler404 = users.views.page_not_found
handler500 = users.views.page_error

urlpatterns = [
    # url(r'^users/', include('users.urls')),
    url('xadmin/', xadmin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace="rest_framework")),
    url(r'^courses/', include('courses.urls')),
    url(r'^sources/', include('sources.urls')),
    # url(r'docs/', include_docs_urls(title="AIGIS")),
    url(r'docs/', schema_view),
    url(r'^wechat', include('wechat.urls')),
    url(r'^', include('users.urls')),

    ## 增加以下一行，以识别静态资源
    url(r'^static/(?P<path>.*)$', static.serve,
        {'document_root': settings.STATIC_ROOT}, name='static'),

]
