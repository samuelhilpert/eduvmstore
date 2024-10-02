from rest_framework import serializers

class AppTemplateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    description = serializers.CharField()
    image_id = serializers.CharField(max_length=255)
    visibility = serializers.CharField(max_length=20)
