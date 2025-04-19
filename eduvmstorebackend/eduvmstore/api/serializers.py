import logging
from django.utils.timezone import now
from typing import Dict, List

from rest_framework import serializers
from eduvmstore.db.models import (AppTemplates, Users, Roles, AppTemplateInstantiationAttributes,
                                  AppTemplateAccountAttributes, Favorites, AppTemplateSecurityGroups)
from eduvmstore.utils.string_utils import has_version_suffix, extract_version_suffix

logger = logging.getLogger("eduvmstore_logger")
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

class AppTemplateSecurityGroupsSerializer(serializers.ModelSerializer):
    """Serializer for the AppTemplateSecurityGroups model.

    This serializer handles the conversion of AppTemplateSecurityGroups model
    instances to and from JSON format, including validation and creation of new
    instances.
    """
    class Meta:
        model = AppTemplateSecurityGroups
        fields = ['id', 'name']
        read_only_fields = ['id']

class AppTemplateSerializer(serializers.ModelSerializer):
    """Serializer for the AppTemplates model.

    This serializer handles the conversion of AppTemplates model instances
    to and from JSON format, including validation and creation of new instances.
    """
    instantiation_attributes = AppTemplateInstantiationAttributesSerializer(many=True, read_only=False)
    account_attributes = AppTemplateAccountAttributesSerializer(many=True, read_only=False)
    security_groups = AppTemplateSecurityGroupsSerializer(many=True, read_only=False)

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
            'ssh_user_requested',
            'instantiation_attributes',
            'account_attributes',
            'security_groups',
            'public',
            'approved',

            'volume_size_gb',

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
            'deleted',
            'version'
        ]

    # Validation method for the name field (automatically triggered by Django Rest Framework)
    def validate_name(self, name: str) -> str:
        """
        Validate that the app template name doesn't have a version suffix.

        :param str name: The name to validate
        :return: The validated name
        :raises: ValidationError if name has version suffix
        """
        if has_version_suffix(name):
            suffix = extract_version_suffix(name)
            raise serializers.ValidationError(
                f"App template name cannot end with the version suffix '{suffix}'. "
            )
        return name

    def create_instantiation_attributes(self,
                                        app_template: AppTemplates,
                                        instantiation_attributes_data: List[Dict]) -> None:
        """
        Create AppTemplateInstantiationAttributes instances for an AppTemplate instance.

        :param AppTemplates app_template: The AppTemplate instance to create the attributes for
        :param List instantiation_attributes_data: List of instantiation attribute data
        :return: None
        :rtype: None
        """
        for instantiation_attribute_data in instantiation_attributes_data:
            AppTemplateInstantiationAttributes.objects.create(
                app_template_id=app_template,
                **instantiation_attribute_data)

    def create_account_attributes(self,
                                  app_template: AppTemplates,
                                  account_attributes_data: List[Dict]) -> None:
        """
        Create AppTemplateAccountAttributes instances for an AppTemplate instance.

        :param AppTemplates app_template: The AppTemplate instance to create the attributes for
        :param List[Dict] account_attributes_data: List of instantiation attribute data
        :return: None
        :rtype: None
        """
        for account_attribute_data in account_attributes_data:
            AppTemplateAccountAttributes.objects.create(
                app_template_id=app_template,
                **account_attribute_data)

    def create_security_groups(self,
                               app_template: AppTemplates,
                               security_groups_data: List[Dict]) -> None:
        """
        Create AppTemplateSecurityGroups instances for an AppTemplate instance.

        :param AppTemplates app_template: The AppTemplate instance to create the attributes for
        :param List[Dict] security_groups_data: List of instantiation attribute data
        :return: None
        :rtype: None
        """
        for security_group_data in security_groups_data:
            AppTemplateSecurityGroups.objects.create(
                app_template_id=app_template,
                **security_group_data
            )

    def create(self, validated_data: Dict) -> AppTemplates:
        """
        Custom create method to handle additional operations
        before saving an AppTemplates instance to the database.

        :param Dict validated_data: Data validated through the serializer
        :return: Newly created AppTemplates instance
        :rtype: AppTemplates
        """
        instantiation_attributes_data = validated_data.pop('instantiation_attributes')
        account_attributes_data = validated_data.pop('account_attributes')
        security_groups_data = validated_data.pop('security_groups')
        app_template = AppTemplates.objects.create(**validated_data)
        if instantiation_attributes_data:
            self.create_instantiation_attributes(app_template, instantiation_attributes_data)
        if account_attributes_data:
            self.create_account_attributes(app_template, account_attributes_data)
        if security_groups_data:
            self.create_security_groups(app_template, security_groups_data)
        return app_template

    def update(self, instance: AppTemplates, validated_data: Dict) -> AppTemplates:
        """
        Custom update method to handle additional operations
        before saving an AppTemplates instance to the database. Public AppTemplates
        can't be updated.

        :param AppTemplates instance: The instance to update
        :param Dict validated_data: Data validated through the serializer
        :return: Updated AppTemplates instance
        :rtype: AppTemplates
        """

        if instance.approved:
            raise serializers.ValidationError(
                {"detail": "Approved app templates cannot be "
                           "edited to avoid confusion for other users."
                           "Clone the app template and edit the clone instead."},
                code='forbidden'
            )

        instantiation_attributes_data = validated_data.pop('instantiation_attributes')
        account_attributes_data = validated_data.pop('account_attributes')
        security_groups_data = validated_data.pop('security_groups')


        if instantiation_attributes_data:
            AppTemplateInstantiationAttributes.objects.filter(app_template_id=instance).delete()
            self.create_instantiation_attributes(instance, instantiation_attributes_data)
        if account_attributes_data:
            AppTemplateAccountAttributes.objects.filter(app_template_id=instance).delete()
            self.create_account_attributes(instance, account_attributes_data)
        if security_groups_data:
            AppTemplateSecurityGroups.objects.filter(app_template_id=instance).delete()
            self.create_security_groups(instance, security_groups_data)

        model_fields = {field.name: field for field in instance._meta.fields}
        for field_name, field in model_fields.items():
            if field_name in self.Meta.read_only_fields:
                continue
            elif field_name in validated_data:
                setattr(instance, field_name, validated_data[field_name])
            elif field.has_default():
                setattr(instance, field_name, field.default)

        instance.updated_at = now()
        instance.approved = False
        instance.save()
        return instance

class FavoritesSerializer(serializers.ModelSerializer):
    """Serializer for the Favorite model.

    This serializer handles the conversion of Favorite model instances
    to and from JSON format, including validation and creation of new instances.
    """
    class Meta:
        model = Favorites
        fields = ['id', 'user_id', 'app_template_id']
        read_only_fields = ['id', 'user_id']

    def create(self, validated_data: Dict) -> Favorites:
        """
        Create method to handle additional operations
        before saving a Favorite instance to the database.

        :param dict validated_data: Data validated through the serializer
        :return: Newly created Favorite instance
        :rtype: Favorite
        """
        user_id = validated_data.get('user_id')
        app_template_id = validated_data.get('app_template_id')
        favorite, created = Favorites.objects.get_or_create(
            user_id=user_id,
            app_template_id=app_template_id,
            defaults=validated_data
        )
        return favorite


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

    def create(self, validated_data: Dict) -> Roles:
        """
        Custom create method to handle additional operations
        before saving a Roles instance to the database.

        :param Dict validated_data: Data validated through the serializer
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

    def create(self, validated_data: Dict) -> Users:
        """
        Custom create method to handle additional operations
        before saving a Users instance to the database.

        :param dict validated_data: Data validated through the serializer
        :return: Newly created Users instance
        :rtype: Users
        """
        return Users.objects.create(**validated_data)