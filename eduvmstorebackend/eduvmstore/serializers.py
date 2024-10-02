"""
from rest_framework import serializers
from .models import AppTemplate

class AppTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppTemplate
        fields = '__all__'

"""