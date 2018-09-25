from django.shortcuts import render

# Create your views here.

from sources.models import SourcesCore
from api.serializers import SourcesCoreSerializers

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,mixins,generics,viewsets,filters


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
        商品分类列表数据
    retrieve:
        获取商品分类详情
    """
    queryset = SourcesCore.objects.filter(question_type=2)
    serializer_class = SourcesCoreSerializers
