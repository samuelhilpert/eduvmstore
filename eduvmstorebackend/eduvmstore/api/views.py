
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from eduvmstore.services.glance_service import list_images
from eduvmstore.api.serializers import AppTemplateSerializer, RoleSerializer, UserSerializer
from eduvmstore.db.models import AppTemplates, Roles, Users
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from eduvmstore.db.operations.app_templates import (create_app_template,
                                                    list_app_templates,
                                                    approve_app_template,
                                                    check_app_template_name_collisions,
                                                    soft_delete_app_template)
from eduvmstore.db.operations.users import get_user_by_id

from eduvmstore.services.app_template_service import get_image_id_from_app_template, get_default_network_id
from eduvmstore.services.nova_service import create_instance


# from eduvmstore.db.operations.app_templates import create_app_template, list_app_templates


class AppTemplateViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling AppTemplate model operations.

    This ViewSet provides default CRUD operations for the AppTemplates model,
    including custom actions for approving templates and checking name collisions.

    :param queryset: Queryset of AppTemplates instances, filtered to exclude deleted ones
    :param serializer_class: Serializer class for AppTemplates model
    """
    queryset = AppTemplates.objects.filter(deleted=False)
    serializer_class = AppTemplateSerializer

    def perform_create(self, serializer):
        """
        Custom handle creation of an AppTemplates instance with initial field values.

        :param AppTemplateSerializer serializer: Serializer for the AppTemplates model
        :return: None
        :rtype: None
        """
        serializer.save(creator_id=self.request.myuser, approved=False)
        # creator_id: Ensures that the creator_id is set to the ID of the authenticated user

    def get_queryset(self):
        """
        Custom retrieval of the queryset of AppTemplates,
        optionally filtered by search, public, and approved status.

        :return: Filtered queryset of AppTemplates
        :rtype: QuerySet
        """
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
        """
        Custom endpoint to approve an AppTemplate.

        :param Request request: The HTTP request object
        :param str pk: Primary key of the AppTemplate to approve
        :return: HTTP response with the approval status
        :rtype: Response
        """
        app_template_id = self.get_object().id
        app_template = approve_app_template(app_template_id)
        return Response(
            {"id": app_template.id, "approved": app_template.approved},
            status=status.HTTP_200_OK)

    # action decorator for custom endpoint
    # detail = False means it is for all AppTemplate
    @action(detail=False, methods=['get'], url_path='name/(?P<name>[^/.]+)\\/collisions',
            name='check-name-collisions')
    def check_name_collisions(self, request, name=None):
        """
        Custom endpoint to check for name collisions in AppTemplates.

        :param Request request: The HTTP request object
        :param str name: Name to check for collisions
        :return: HTTP response with collision status
        :rtype: Response
        """
        collisions = check_app_template_name_collisions(name)

        response_object = {"name": name, "collisions": collisions}
        return Response(response_object, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        """
        Soft delete an AppTemplate by setting its deleted flag and timestamp.

        :param AppTemplates instance: The AppTemplates instance to delete
        :return: HTTP response with no content
        :rtype: Response
        """
        soft_delete_app_template(self.get_object().id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling Users model operations.

    This ViewSet provides default CRUD operations for the Users model.

    :param queryset: Queryset of Users instances, filtered to exclude deleted ones
    :param serializer_class: Serializer class for Users model
    """
    queryset = Users.objects.filter(deleted=False)
    serializer_class = UserSerializer

    def retrieve(self, request, pk=None):
        """
        Retrieve details of a specific user with role information.

        :param Request request: The HTTP request object
        :param str pk: The unique identifier of the user (primary key)
        :return: HTTP response with a placeholder message
        :rtype: Response
        """
        try:
            user = get_user_by_id(pk)
        except ObjectDoesNotExist:
            return Response({"detail": f"User with id \"{pk}\" not found"},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RoleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling Roles model operations.

    This ViewSet provides default CRUD operations for the Roles model.

    :param queryset: Queryset of all Roles instances
    :param serializer_class: Serializer class for Roles model
    """
    queryset = Roles.objects.all()
    serializer_class = RoleSerializer


# normal ViewSet chosen, as Images are not part of own database
class ImageViewSet(viewsets.ViewSet):
    """
    ViewSet for handling image operations.

    This ViewSet provides OpenStack access to glance images.

    :param list: Method to list all images
    :param retrieve: Method to retrieve details of a specific image
    """

    def list(self, request):
        """
        List all images (placeholder implementation).

        :param Request request: The HTTP request object
        :return: HTTP response with a placeholder message
        :rtype: Response
        """
        token = request.headers.get('X-Auth-Token')
        if not token:
            return Response({"error": "Authorization token missing"},
                            status=status.HTTP_401_UNAUTHORIZED)

        try:
            images = list_images(token)
            return Response(images,
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Django passes id automatically as pk
    def retrieve(self, request, pk):
        """
         Retrieve details of a specific image (placeholder implementation).

         :param Request request: The HTTP request object
         :param str pk: The unique identifier of the image (primary key)
         :return: HTTP response with a placeholder message
         :rtype: Response
         """
        print("id: ", pk)
        # Placeholder logic to return details of a specific image
        return Response({"message": "Not yet implemented"}, status=status.HTTP_200_OK)


# normal ViewSet chosen, as Flavors are not part of own database
class FlavorViewSet(viewsets.ViewSet):
    """
    ViewSet for handling flavor operations.

    This ViewSet gives a selection from the current flavors in OpenStack.

    :param select_flavor: Method to return possible and best matching flavors
    """
    # action decorator for custom endpoint
    # detail = False means it is for all AppTemplate
    @action(detail=False, methods=['post'], url_path='selection')
    def select_flavor(self, request):
        """
        Return possible and best matching flavors (placeholder implementation).

        :param Request request: The HTTP request object
        :return: HTTP response with best and possible flavor IDs
        :rtype: Response
        """

        # Retrieve All possible flavors from OpenStack

        # Filter Flavors not matching any of the required parameters of the app template and openstack
        # get app template minimal requirements
        # Query Nova Service for available user ressource (instance count, RAM, CPU, Disk)
        # check for each flavor if it is larger than the requirements


        # Placeholder logic to return possible and best matching flavors
        return Response({"best_flavor_id": None, "possible_flavor_ids": []},
                        status=status.HTTP_200_OK)


# normal ViewSet chosen, as Instances are not part of own database
class InstanceViewSet(viewsets.ViewSet):
    """ViewSet for handling instance operations.

    This ViewSet provides access to OpenStack Instances.

    :param perform_create: Method to create an instance
    """
    # action decorator for custom endpoint
    # detail = False means it is for all AppTemplate

    @action(detail=False, methods=['post'], url_path='launch')
    def perform_create(self, request):
        """
        Create an instance (placeholder implementation).

        :param Request request: The HTTP request object
        :return: HTTP response with instance ID and accounts
        :rtype: Response
        """
        print('Entered perform_create')
        token = request.headers.get('X-Auth-Token')
        if not token:
            return Response({"error": "Authorization token missing"},
                            status=status.HTTP_401_UNAUTHORIZED)

        name = request.data.get('name')
        network_id = request.data.get('network_id')
        app_template_id = request.data.get('app_template_id')
        flavor_id = request.data.get('flavor_id')
        accounts = request.data.get('accounts')

        print('name:', name)

        if not all([name, network_id, app_template_id, flavor_id]):
            return Response({"error": "Missing required parameters"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            image_id = get_image_id_from_app_template(app_template_id)
            print('image_id:', image_id)
            # TODO: network_id currently handed over from frontend should be requested from openstack
            # network_id = get_default_network_id(token)
            instance = create_instance(name, image_id, flavor_id, network_id, token)
            return Response({"id": instance.id, "name": instance.name}, status=status.HTTP_201_CREATED)
            # return Response({"message": "not yet implemented"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
