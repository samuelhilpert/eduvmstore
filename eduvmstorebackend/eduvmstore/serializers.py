from rest_framework import serializers

class AppTemplateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=500)
    image = serializers.CharField(max_length=255)
    created_at = serializers.DateTimeField()

    def create(self, validated_data):
        from eduvmstorebackend.eduvmstore.db.models import AppTemplate
        return AppTemplate(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        return instance
