from django.urls import path
from .views import AppTemplateViewSet, UserViewSet, RoleViewSet, FavoritesViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'app-templates', AppTemplateViewSet, basename='app-template')
router.register(r'users', UserViewSet, basename='user')
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'favorites', FavoritesViewSet, basename='favorite')

urlpatterns = [
    *router.urls,
    path('app-templates/name/<str:name>/collision/',
         AppTemplateViewSet.as_view({'get': 'check_name_collision'}),
         name='check-name-collision'),
]
