# -*-coding:utf-8 -*-
__author__ = 'Cenergy'
__date__ = '10/8/18 下午4:26'


from rest_framework import serializers

from .models import SourcesCore

###SourcesCore

class  SourcesCoreSerializers(serializers.ModelSerializer):
    class Meta:
        model = SourcesCore
        fields="__all__"

