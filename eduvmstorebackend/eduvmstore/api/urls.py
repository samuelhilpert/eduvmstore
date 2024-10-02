from django.urls import path
from .views import AppTemplateViewSet, InstanceListAPI, ImageListAPI

urlpatterns = [
    path('app-templates/', AppTemplateViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('images/', ImageListAPI.as_view(), name='image-list'),
]
