"""
from django.db import models

# Create your models here.

class AppTemplate(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
"""