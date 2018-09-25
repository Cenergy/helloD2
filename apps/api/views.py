from django.shortcuts import render

# Create your views here.

from sources.models import SourcesCore
from api.serializers import SourcesCoreSerializers

from rest_framework.views import APIView
from rest_framework.response import Response


class SnippetList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        snippets = SourcesCore.objects.all()
        serializer = SourcesCoreSerializers(snippets, many=True)
        return Response(serializer.data)
