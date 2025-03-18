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
