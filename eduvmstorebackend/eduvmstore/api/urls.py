from django.urls import path
from .views import AppTemplateViewSet, UserViewSet, RoleViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'app-templates', AppTemplateViewSet, basename='app-template')
router.register(r'users', UserViewSet, basename='user')
router.register(r'roles', RoleViewSet, basename='role')

urlpatterns = [
    *router.urls,
    path('app-templates/name/<str:name>/collisions/',
         AppTemplateViewSet.as_view({'get': 'check_name_collisions'}),
         name='check-name-collisions'),
]
