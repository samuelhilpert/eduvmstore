from rest_framework import serializers
from eduvmstore.db.models import AppTemplates, Users, Roles, AppTemplateInstantiationAttributes

class AppTemplateInstantiationAttributesSerializer(serializers.ModelSerializer):
    """Serializer for the AppInstantiationAttributes model.

    This serializer handles the conversion of AppTemplateInstantiationAttributes model
    instances to and from JSON format, including validation and creation of new
    instances.
    """
    class Meta:
        model = AppTemplateInstantiationAttributes
        fields = ['id', 'name']
        read_only_fields = ['id']

class AppTemplateSerializer(serializers.ModelSerializer):
    """Serializer for the AppTemplates model.

    This serializer handles the conversion of AppTemplates model instances
    to and from JSON format, including validation and creation of new instances.
    """
    instantiation_attributes = AppTemplateInstantiationAttributesSerializer(many=True, read_only=False)

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
            'instantiation_attributes',
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
        instantiation_attributes_data = validated_data.pop('instantiation_attributes')
        app_template = AppTemplates.objects.create(**validated_data)
        for instantiation_attribute_data in instantiation_attributes_data:
            AppTemplateInstantiationAttributes.objects.create(
                app_template_id=app_template,
                **instantiation_attribute_data)
        return app_template
        # return AppTemplates.objects.create(**validated_data)
    def update(self, instance, validated_data):
        """
        Custom update method to handle additional operations
        before saving an AppTemplates instance to the database.

        :param AppTemplates instance: The instance to update
        :param dict validated_data: Data validated through the serializer
        :return: Updated AppTemplates instance
        :rtype: AppTemplates
        """

        instantiation_attributes_data = validated_data.pop('instantiation_attributes')
        if instantiation_attributes_data:
            # Update instantiation attributes by deleting all and creating only the new ones
            AppTemplateInstantiationAttributes.objects.filter(app_template_id=instance).delete()
            for instantiation_attribute_data in instantiation_attributes_data:
                AppTemplateInstantiationAttributes.objects.create(
                    app_template_id=instance,
                    **instantiation_attribute_data)

        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.short_description = validated_data.get('short_description', instance.short_description)
        instance.instantiation_notice = validated_data.get('instantiation_notice',
                                                           instance.instantiation_notice)
        instance.script = validated_data.get('script', instance.script)
        instance.image_id = validated_data.get('image_id', instance.image_id)
        instance.version = validated_data.get('version', instance.version)
        instance.public = validated_data.get('public', instance.public)
        instance.approved = False
        instance.fixed_ram_gb = validated_data.get('fixed_ram_gb', instance.fixed_ram_gb)
        instance.fixed_disk_gb = validated_data.get('fixed_disk_gb', instance.fixed_disk_gb)
        instance.fixed_cores = validated_data.get('fixed_cores', instance.fixed_cores)
        instance.per_user_ram_gb = validated_data.get('per_user_ram_gb', instance.per_user_ram_gb)
        instance.per_user_disk_gb = validated_data.get('per_user_disk_gb', instance.per_user_disk_gb)
        instance.per_user_cores = validated_data.get('per_user_cores', instance.per_user_cores)
        instance.save()
        return instance


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