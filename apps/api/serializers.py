# -*-coding:utf-8 -*-
__author__ = 'Cenergy'
__date__ = '25/9/18 上午9:35'


# -*-coding:utf-8 -*-
__author__ = 'Cenergy'
__date__ = '10/8/18 下午4:26'


from rest_framework import serializers

from sources.models import SourcesCore

###SourcesCore

class  SourcesCoreSerializers(serializers.ModelSerializer):
    def validate(self, attrs):
        attrs["mobile"] = attrs["sourcename"]
        del attrs["code"]
        return attrs

    class Meta:
        model = SourcesCore
        fields="__all__"
