from rest_framework import serializers
from eduvmstore.db.models import AppTemplates, Users, Roles

class AppTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppTemplates
        fields = [
            'id',
            'creator_id',
            'created_at',
            'updated_at',

            'image_id',
            'name',
            'description',
            'short_description',
            'instantiation_notice',
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
        read_only_fields = [
            'id',
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
        return AppTemplates.objects.create(**validated_data)



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = [
            'id',
            'created_at',
            'updated_at',
            'role_id'
        ]
        read_only_fields = [
            'id',
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
        return Users.objects.create(**validated_data)


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = [
            'id',
            'name',
            'access_level'
        ]
        read_only_fields = [
            'id'
        ]

    def create(self, validated_data):
        """
        Custom create method if you need to perform additional
        operations before saving an instance.
        """
        return Roles.objects.create(**validated_data)

