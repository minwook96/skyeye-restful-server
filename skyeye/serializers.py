from rest_framework import serializers
from .models import *


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = '__all__'


class SiteSettingsConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettingsConfig
        fields = '__all__'
