import uuid

from django.db import models

from django.utils.timezone import now


class AppTemplates(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image_id = models.UUIDField(db_index=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=255)
    instantiation_notice = models.TextField(blank=True, null=True)
    script = models.TextField(blank=True, null=True)
    ssh_user_requested = models.BooleanField(default=False)

    # CRUD info
    creator_id = models.ForeignKey('Users', on_delete=models.DO_NOTHING, db_index=True)
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(default=now)
    # soft delete currenly unused, potential enhancement for the future
    deleted_at = models.DateTimeField(null=True)
    deleted = models.BooleanField(default=False)
    version = models.IntegerField(default=1) # versioning for approval naming

    # visibility
    public = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)

    # volume
    volume_size_gb = models.FloatField(null=True, default=None)

    # resource requirements
    fixed_ram_gb = models.FloatField()
    fixed_disk_gb = models.FloatField()
    fixed_cores = models.FloatField()
    per_user_ram_gb = models.FloatField()
    per_user_disk_gb = models.FloatField()
    per_user_cores = models.FloatField()

    def __str__(self):
        return self.name

class AppTemplateInstantiationAttributes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    app_template_id = (
        models.ForeignKey(AppTemplates, on_delete=models.CASCADE, related_name='instantiation_attributes'))
    name = models.CharField(max_length=255)

    # No CRUD Info as AppTemplateInstantiationAttributes are strongly bound to AppTemplates
    # Due to the strong bound, there is no dedicated db-operation file to access
    # instantiation attributes alone
    def __str__(self):
        return self.name

class AppTemplateAccountAttributes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    app_template_id = (
        models.ForeignKey(AppTemplates, on_delete=models.CASCADE, related_name='account_attributes'))
    name = models.CharField(max_length=255)

    # No CRUD Info as AppTemplateAccountAttributes are strongly bound to AppTemplates
    # Due to the strong bound, there is no dedicated db-operation file to access
    # account attributes alone
    def __str__(self):
        return self.name

class AppTemplateSecurityGroups(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    app_template_id = (
        models.ForeignKey(AppTemplates, on_delete=models.CASCADE, related_name='security_groups'))
    name = models.CharField(max_length=255)

    # No CRUD Info as AppTemplateSecurityGroups are strongly bound to AppTemplates
    # Due to the strong bound, there is no dedicated db-operation file to access
    # security groups alone
    def __str__(self):
        return self.name

class Users(models.Model):
    # default needs to be deleted, the moment, we get the user from keystone/token
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role_id = models.ForeignKey('Roles', on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=True)

    # CRUD info
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)
    deleted_at = models.DateTimeField(null=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

class Roles(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    access_level = models.IntegerField()

    def __str__(self):
        return self.name

class Favorites(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    app_template_id = models.ForeignKey(AppTemplates, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'app_template_id'],
                                    name='unique_user_app_template',
                                    violation_error_message='User already has this app template in favorites'
                                    )
        ]

    def __str__(self):
        return str(self.user_id)
