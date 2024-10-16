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

    # CRUD info
    creator_id = models.ForeignKey('Users', on_delete=models.DO_NOTHING, db_index=True)
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(default=now)
    deleted_at = models.DateTimeField(null=True)
    deleted = models.BooleanField(default=False)

    # version and visibility
    version = models.CharField(max_length=50, default="1.0")
    public = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)

    # resource requirements
    fixed_ram_gb = models.FloatField()
    fixed_disk_gb = models.FloatField()
    fixed_cores = models.FloatField()
    per_user_ram_gb = models.FloatField()
    per_user_disk_gb = models.FloatField()
    per_user_cores = models.FloatField()

    def __str__(self):
        return self.name


class Users(models.Model):
    # default needs to be deleted, the moment, we get the user from keystone/token
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role_id = models.ForeignKey('Roles', on_delete=models.DO_NOTHING)

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
