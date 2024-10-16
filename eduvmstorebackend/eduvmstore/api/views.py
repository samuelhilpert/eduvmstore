from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView

from django.utils.timezone import now
from django.db.models import Q

# from eduvmstore.services.glance_service import list_images
from eduvmstore.api.serializers import AppTemplateSerializer, UserSerializer, RoleSerializer
from eduvmstore.db.models import AppTemplates, Users, Roles
# from eduvmstore.db.operations.app_templates import create_app_template, list_app_templates


class AppTemplateViewSet(viewsets.ModelViewSet):
    queryset = AppTemplates.objects.filter(deleted=False)
    serializer_class = AppTemplateSerializer

    def perform_create(self, serializer):
        serializer.save(approved=False)
    #     # Setzt das Feld 'creator_id' auf die ID des aktuell authentifizierten Benutzers
    #     serializer.save(creator_id=self.request.user.id)

    def get_queryset(self):
        queryset = AppTemplates.objects.filter(deleted=False)

        # Get query parameter
        search = self.request.query_params.get('search', None)
        public = self.request.query_params.get('public', None)
        approved = self.request.query_params.get('approved', None)

        if search:
            # Search
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(short_description__icontains=search) |
                Q(instantiation_notice__icontains=search) |
                Q(version__icontains=search) |
                Q(id__icontains=search)
            )

        # Filter
        if public is not None:
            queryset = queryset.filter(public=public)
        if approved is not None:
            queryset = queryset.filter(approved=approved)

        return queryset

    # action decorator for custom endpoint
    # detail = True means it is for a specific AppTemplate
    @action(detail=True, methods=['patch'])
    def approved(self, request, pk=None):
        app_template = self.get_object()
        app_template.approved = True
        app_template.save()
        return Response(
            {"id": app_template.id, "approved": app_template.approved},
            status=status.HTTP_200_OK)

    # action decorator for custom endpoint
    # detail = False means it is for all AppTemplate
    @action(detail=False, methods=['get'], url_path='name/(?P<name>[^/.]+)\\/collisions')
    def check_name_collisions(self, request, name=None):
        # Check for name collisions
        collisions = AppTemplates.objects.filter(name=name, deleted=False).exists()

        response_object = {"name": name, "collisions": collisions}
        return Response(response_object, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        app_template = self.get_object()
        app_template.deleted = True
        app_template.deleted_at = now()
        app_template.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.filter(deleted=False)
    serializer_class = UserSerializer


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Roles.objects.all()
    serializer_class = RoleSerializer

# normal ViewSet chosen, as Images are not part of own database
class ImageViewSet(viewsets.ViewSet):

    def list(self, request):
        return Response(
            [{"message": "not yet implemented"}],
            status=status.HTTP_200_OK
        )

    def retrieve(self, request, id):
        print("id: ",id)
        # Placeholder logic to return details of a specific image
        return Response({"message": "Not yet implemented"}, status=status.HTTP_200_OK)

# normal ViewSet chosen, as Flavors are not part of own database
class FlavorViewSet(viewsets.ViewSet):
    def select_flavor(self, request):
        # Placeholder logic to return possible and best matching flavors
        return Response({"best_flavor_id": None, "possible_flavor_ids": []}, status=status.HTTP_200_OK)

# normal ViewSet chosen, as Instances are not part of own database
class InstanceViewSet(viewsets.ViewSet):
    def perform_create(self, request):
        # Placeholder logic to create an instance
        return Response({"id": None, "accounts": [] }, status=status.HTTP_201_CREATED)