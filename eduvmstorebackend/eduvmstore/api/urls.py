from django.urls import path
from .views import AppTemplateViewSet, ImageListAPI, TestAPI, UserViewSet, RoleViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'app-templates', AppTemplateViewSet, basename='app-template')
router.register(r'users', UserViewSet, basename='user')
router.register(r'roles', RoleViewSet, basename='role')

urlpatterns = router.urls

# urlpatterns = [
#     path('app-templates/', AppTemplateViewSet.as_view({'get': 'list', 'post': 'create'})),
#     path('images/', ImageListAPI.as_view(), name='image-list'),
#     path('test/', TestAPI.as_view(), name='test'),
#     path('users/', UserViewSet.as_view({'get': 'list'})),
# ]
