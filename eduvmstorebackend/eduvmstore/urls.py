"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AppTemplateViewSet

router = DefaultRouter()
router.register(r'app_templates', AppTemplateViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
"""