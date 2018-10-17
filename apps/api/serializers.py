# -*-coding:utf-8 -*-
__author__ = 'Cenergy'
__date__ = '25/9/18 上午9:35'


# -*-coding:utf-8 -*-
__author__ = 'Cenergy'
__date__ = '10/8/18 下午4:26'


from rest_framework import serializers

from sources.models import SourcesCore
from users.models import Suggestion

from courses.models import Blog

###SourcesCore

class  SourcesCoreSerializers(serializers.ModelSerializer):
    class Meta:
        model = SourcesCore
        fields="__all__"

class  SuggestionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Suggestion
        fields="__all__"


class BlogSerializers(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields="__all__"