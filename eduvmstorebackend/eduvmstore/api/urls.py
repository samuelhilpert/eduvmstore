from django.urls import path
from .views import AppTemplateViewSet, ImageListAPI, TestAPI, UserViewSet

urlpatterns = [
    path('app-templates/', AppTemplateViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('images/', ImageListAPI.as_view(), name='image-list'),
    path('test/', TestAPI.as_view(), name='test'),
    path('user/', UserViewSet.as_view({'post': 'create'})),
]
