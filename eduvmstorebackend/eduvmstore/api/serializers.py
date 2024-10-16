from rest_framework import serializers
from eduvmstore.db.models import AppTemplate, User, Role

class AppTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppTemplate
        fields = [
            'id',
            'image_id',
            'name',
            'description',
            'short_description',
            'instantiation_notice',
            'creator_id',
            'created_at',
            'updated_at',
            'deleted_at',
            'deleted',
            'version',
            'public',
            'approved',
            'fixed_ram_gb',
            'fixed_disk_gb',
            'fixed_cores',
            'per_user_ram_gb',
            'per_user_disk_gb',
            'per_user_cores'
        ]

    def create(self, validated_data):
        """
        Custom create method if you need to perform additional
        operations before saving an instance.
        """
        return AppTemplate.objects.create(**validated_data)



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'role',
            'created_at',
            'updated_at',
            'deleted_at',
            'deleted'
        ]

    def create(self, validated_data):
        """
        Custom create method if you need to perform additional
        operations before saving an instance.
        """
        return User.objects.create(**validated_data)


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = [
            'id',
            'name',
            'access_level'
        ]

    def create(self, validated_data):
        """
        Custom create method if you need to perform additional
        operations before saving an instance.
        """
        return Role.objects.create(**validated_data)