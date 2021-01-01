from django.shortcuts import render, get_object_or_404
import math

# Create your views here.


from api.serializers import SourcesCoreSerializers, BlogSerializers

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, mixins, generics, viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db import connection

from .filters import SourcesCoreFilter
from utils.email_send import register_send_email, common_send_email
from sources.models import SourcesCore
from users.models import Suggestion
from courses.models import Blog, BlogType

import pandas as pd


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000
    page_query_param = "page"


class SnippetList(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def get(self, request, format=None):
        print(request.query_params, "------------")
        question_type = request.query_params.get("question_type", -1)
        page_info = request.query_params.get("page", 1)
        limit_info = request.query_params.get("limit", 10)
        key_word = request.query_params.get("key[id]", False)
        if int(page_info) == 1:
            page_start = int(page_info)
        else:
            max_info = int(page_info) * int(limit_info)
            page_start = max_info - int(limit_info) + 1
        if key_word:
            query_sql0 = "SELECT * FROM sources_sourcescore where sourcename like '%{0}%'".format(
                key_word)
            datas = pd.read_sql(query_sql0, connection)
            count = len(datas)
            query_sql = "SELECT * FROM sources_sourcescore where sourcename like '%{0}%'  LIMIT {1},{2} ".format(
                key_word, page_start - 1, int(limit_info))
        else:
            count_sql = "SELECT * FROM sources_sourcescore where question_type={0}".format(
                question_type)
            datas = pd.read_sql(count_sql, connection)
            count = len(datas)
            query_sql = "SELECT * FROM sources_sourcescore where question_type={0} LIMIT {1},{2}".format(question_type,
                                                                                                         page_start - 1,
                                                                                                         int(
                                                                                                             limit_info))
        snippets = SourcesCore.objects.raw(query_sql)
        serializer = SourcesCoreSerializers(snippets, many=True)
        data = {"code": 0, "msg": "", "count": count, "data": serializer.data}
        return Response(data)


# 这个能分页的那种
class SourcesListView(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def get(self, request, format=None):
        page = request.query_params.get("page", 1)
        num = request.query_params.get("num", 10)
        key_word = request.query_params.get("key_word", False)
        objStart = (int(page)-1)*int(num)
        objEnd = int(page)*int(num)

        if key_word:
            query_sql = "SELECT * FROM sources_sourcescore where sourcename like '%{0}%'LIMIT {1},{2} ".format(
                key_word, objStart, objEnd)
            datas = pd.read_sql(query_sql, connection)
            count = len(datas)
        else:
            count_sql = "SELECT * FROM sources_sourcescore "
            datas = pd.read_sql(count_sql, connection)
            count = len(datas)
            # SELECT * FROM sources_sourcescore LIMIT  10 offset 1
            query_sql = "SELECT * FROM sources_sourcescore LIMIT  {1} offset {0}".format(
                objStart, num)
            print(query_sql,"==============")
        snippets = SourcesCore.objects.raw(query_sql)
        serializer = SourcesCoreSerializers(snippets, many=True)
        pages = math.ceil(int(count)/int(num))
        data = {"code": 0, "msg": "", "pages": pages,
                "count": count, "data": serializer.data}
        return Response(data)


class SourcesList(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def get(self, request, format=None):
        print(request.query_params)
        question_type = request.query_params.get("question_type", -1)
        key_word = request.query_params.get("key_word", False)
        if key_word:
            query_sql = "SELECT * FROM sources_sourcescore where sourcename like '%{0}%'".format(
                key_word)
            datas = pd.read_sql(query_sql, connection)
            count = len(datas)
        else:
            if int(question_type) == -1:
                count_sql = "SELECT * FROM sources_sourcescore"
                datas = pd.read_sql(count_sql, connection)
                count = len(datas)
                query_sql = "SELECT * FROM sources_sourcescore"
            else:
                count_sql = "SELECT * FROM sources_sourcescore where question_type={0}".format(
                    question_type)
                datas = pd.read_sql(count_sql, connection)
                count = len(datas)
                query_sql = "SELECT * FROM sources_sourcescore where question_type={0}".format(
                    question_type)
        snippets = SourcesCore.objects.raw(query_sql)
        serializer = SourcesCoreSerializers(snippets, many=True)
        data = {"code": 0, "msg": "", "count": count, "data": serializer.data}
        return Response(data)


class SourcesCoreViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        资源分类列表数据
    retrieve:
        获取资源分类详情
    """

    queryset = SourcesCore.objects.all()
    pagination_class = StandardResultsSetPagination
    serializer_class = SourcesCoreSerializers
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    # filter_fields = ('question_type', 'sourcename')
    filter_class = SourcesCoreFilter
    search_fields = ('sourcename',)


class SuggestionsView(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def post(self, request, format=None):
        try:
            suggest_email = request.data.get("suggest_email", None)
            suggest_user = request.data.get("suggest_user", None)
            suggest_message = request.data.get("suggest_message", None)
            if suggest_email == None or suggest_user == None or suggest_message == None:
                reginfs = {
                    "code": 400,
                    "message": "failed",
                    "data": "邮箱，用户名，反馈信息一个都不能为空"
                }
                return Response(reginfs)
            suggest_data = Suggestion()
            suggest_data.email = suggest_email
            suggest_data.suggest_name = suggest_user
            suggest_data.suggest_content = suggest_message
            suggest_data.save()
            # 发邮件回复用户已收到
            common_send_email("673598118@qq.com",
                              suggest_email, suggest_message)
            reginfs = {
                "code": 202,
                "message": "success",
                "data": "恭喜，成功了"
            }
        except:
            reginfs = {
                "code": 400,
                "message": "failed",
                "data": "失败"
            }
        return Response(reginfs)


# 博客
class BlogListView(APIView):
    """
    blog列表
    """

    def get(self, request):
        try:
            contexts = Blog.objects.all().order_by('-id')
            serializer = BlogSerializers(contexts, many=True)
            context = {"code": 0, "msg": "success", "data": serializer.data}
        except:
            context = {
                "code": 200,
                "message": "failed",
                "data": "失败"
            }
        return Response(context)


class BlogDetailView(APIView):
    """
    blog详情
    """

    def get(self, requset, blog_pk):
        try:
            contexts = Blog.objects.filter(id=blog_pk)
            if contexts.exists():
                serializer = BlogSerializers(contexts, many=True)
                context = {"code": 200, "msg": "success",
                           "data": serializer.data}
            else:
                context = {"code": 200, "msg": "请求数据不存在", "data": []}
        except:
            context = {
                "code": 401,
                "message": "failed",
                "data": "失败"
            }
        return Response(context)


class BlogTypeView(APIView):
    def get(self, requset, blog_type):
        try:
            blog_tp = BlogType.objects.filter(id=blog_type)
            contexts = Blog.objects.filter(blog_type=blog_tp)
            if contexts.exists():
                serializer = BlogSerializers(contexts, many=True)
                context = {"code": 200, "msg": "success",
                           "data": serializer.data}
            else:
                context = {"code": 200, "msg": "请求数据不存在哦0!!!", "data": []}
        except:
            context = {
                "code": 401,
                "message": "failed",
                "data": "失败!!"
            }
        return Response(context)

class  JwtLoginView(APIView):
    def post(self, request):
        username = request.POST.get("username", "")
        username = username.lower()
        password = request.POST.get("password", "")
        res = {
            "code": 401,
            "message": "删除失败"
        }
        return  Response(res)