from django.shortcuts import render

# Create your views here.

from sources.models import SourcesCore
from api.serializers import SourcesCoreSerializers

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,mixins,generics,viewsets,filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend



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
        snippets = SourcesCore.objects.all()
        serializer = SourcesCoreSerializers(snippets, many=True)
        return Response(serializer.data)
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
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('question_type', 'sourcename')
