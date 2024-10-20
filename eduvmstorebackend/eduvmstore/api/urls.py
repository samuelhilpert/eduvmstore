from django.urls import path, include
from .views import AppTemplateViewSet, ImageViewSet, UserViewSet, RoleViewSet, FlavorViewSet, InstanceViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'app-templates', AppTemplateViewSet, basename='app-template')
router.register(r'users', UserViewSet, basename='user')
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'images', ImageViewSet, basename='image')
router.register(r'flavors', FlavorViewSet, basename='flavor')
router.register(r'instances', InstanceViewSet, basename='instance')

urlpatterns = [
    *router.urls,
    path('app-templates/name/<str:name>/collisions/',
         AppTemplateViewSet.as_view({'get': 'check_name_collisions'}),
         name='check-name-collisions'),
    path('users/<int:pk>/role/',
         UserViewSet.as_view({'patch': 'change_role'}),
         name='change-role'),
    path('flavors/selection/',
         FlavorViewSet.as_view({'post': 'select_flavor'}),
         name='flavor-selection'),
    path('instances/launch/',
         InstanceViewSet.as_view({'post': 'perform_create'}),
         name='instance-creation'),
]

# urlpatterns = [
#     path('', include(router.urls)),
#     path('images/',
#          ImageViewSet.as_view({'get': 'list'}),
#          name='image-list'),
#     path('images/<str:id>/',
#          ImageViewSet.as_view({'get': 'retrieve'}),
#          name='image-detail'),
#     path('flavors/selection/',
#          FlavorViewSet.as_view({'post': 'select_flavor'}),
#          name='flavor-selection'),
#     path('instances/launch/',
#          InstanceViewSet.as_view({'post': 'perform_create'}),
#          name='instance-creation'),
# ]
