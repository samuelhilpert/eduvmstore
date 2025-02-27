from rest_framework import serializers
from eduvmstore.db.models import AppTemplates, Users, Roles, AppTemplateAccountAttributes

class AppTemplateAccountAttributesSerializer(serializers.ModelSerializer):
    """Serializer for the AppAccountAttributes model.

    This serializer handles the conversion of AppTemplateAccountAttributes model
    instances to and from JSON format, including validation and creation of new
    instances.
    """
    class Meta:
        model = AppTemplateAccountAttributes
        fields = ['id', 'name']
        read_only_fields = ['id']

class AppTemplateSerializer(serializers.ModelSerializer):
    """Serializer for the AppTemplates model.

    This serializer handles the conversion of AppTemplates model instances
    to and from JSON format, including validation and creation of new instances.
    """
    account_attributes = AppTemplateAccountAttributesSerializer(many=True, read_only=False)

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
            'script',
            'account_attributes',
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
            'creator_id',
            'updated_at',
            'deleted_at',
            'deleted'
        ]

    def create(self, validated_data):
        """
        Custom create method to handle additional operations
        before saving an AppTemplates instance to the database.

        :param dict validated_data: Data validated through the serializer
        :return: Newly created AppTemplates instance
        :rtype: AppTemplates
        """
        account_attributes_data = validated_data.pop('account_attributes')
        app_template = AppTemplates.objects.create(**validated_data)
        for account_attribute_data in account_attributes_data:
            AppTemplateAccountAttributes.objects.create(
                app_template=app_template,
                **account_attribute_data)
        return app_template
        # return AppTemplates.objects.create(**validated_data)



class RoleSerializer(serializers.ModelSerializer):
    """Serializer for the Roles model.

    This serializer handles the conversion of Roles model instances
    to and from JSON format, including validation and creation of new instances.
    """
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
        Custom create method to handle additional operations
        before saving a Roles instance to the database.

        :param dict validated_data: Data validated through the serializer
        :return: Newly created Roles instance
        :rtype: Roles
        """
        return Roles.objects.create(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the Users model.

    This serializer handles the conversion of Users model instances
    to and from JSON format, including validation and creation of new instances.
    """
    role = RoleSerializer(source='role_id', read_only=True)

    role_id = serializers.PrimaryKeyRelatedField(queryset=Roles.objects.all(),
                                                 write_only=True,
                                                 required=False)


    class Meta:
            model = Users
            fields = [
                'id',
                'created_at',
                'updated_at',
                'role',
                'role_id',
            ]
            read_only_fields = [
                'id',
                'created_at',
                'updated_at',
                'deleted_at',
                'deleted',
                'is_active',
            ]

    def create(self, validated_data):
        """
        Custom create method to handle additional operations
        before saving a Users instance to the database.

        :param dict validated_data: Data validated through the serializer
        :return: Newly created Users instance
        :rtype: Users
        """
        return Users.objects.create(**validated_data)