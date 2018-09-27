from django.shortcuts import render

# Create your views here.

from sources.models import SourcesCore
from api.serializers import SourcesCoreSerializers

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, mixins, generics, viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from  django.db import connection

from .filters import SourcesCoreFilter
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
        print(request.query_params,"------------")
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
            query_sql0 = "SELECT * FROM sources_sourcescore where sourcename like '%{0}%'".format(key_word)
            datas = pd.read_sql(query_sql0, connection)
            count = len(datas)
            query_sql = "SELECT * FROM sources_sourcescore where sourcename like '%{0}%'  LIMIT {1},{2} ".format(key_word,page_start-1, int(limit_info))
        else:
            count_sql = "SELECT * FROM sources_sourcescore where question_type={0}".format(question_type)
            datas = pd.read_sql(count_sql, connection)
            count = len(datas)
            query_sql = "SELECT * FROM sources_sourcescore where question_type={0} LIMIT {1},{2}" .format(question_type,page_start-1, int(limit_info))
        snippets = SourcesCore.objects.raw(query_sql)
        serializer = SourcesCoreSerializers(snippets, many=True)
        data = {"code": 0, "msg": "", "count": count, "data": serializer.data}
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
            query_sql = "SELECT * FROM sources_sourcescore where sourcename like '%{0}%'".format(key_word)
            datas = pd.read_sql(query_sql, connection)
            count = len(datas)
        else:
            count_sql = "SELECT * FROM sources_sourcescore where question_type={0}".format(question_type)
            datas = pd.read_sql(count_sql, connection)
            count = len(datas)
            query_sql = "SELECT * FROM sources_sourcescore where question_type={0}" .format(question_type)
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
