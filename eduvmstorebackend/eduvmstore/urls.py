from django.urls import path, include
from rest_framework.routers import DefaultRouter
from eduvmstorebackend.eduvmstore.views import AppTemplateViewSet

router = DefaultRouter()
router.register(r'app_templates', AppTemplateViewSet, basename='app_template')

urlpatterns = [
    path('', include(router.urls)),
]
