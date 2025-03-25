
import logging
from django.db.models import Q, QuerySet
from django.core.exceptions import ObjectDoesNotExist
from typing_extensions import override

from eduvmstore.api.serializers import (AppTemplateSerializer, FavoritesSerializer,
                                        UserSerializer, RoleSerializer)
from eduvmstore.db.models import AppTemplates, Favorites, Users, Roles
from eduvmstore.config.access_levels import REQUIRED_ACCESS_LEVELS
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from eduvmstore.db.operations.app_templates import (approve_app_template,
                                                    check_app_template_name_collisions,
                                                    reject_app_template)


logger = logging.getLogger('eduvmstore_logger')
class AppTemplateViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling AppTemplate model operations.

    This ViewSet provides default CRUD operations for the AppTemplates model,
    including custom actions for approving templates and checking name collisions.

    :param serializer_class: Serializer class for AppTemplates model
    """
    serializer_class = AppTemplateSerializer

    @override
    def perform_create(self, serializer) -> None:
        """
        Create an AppTemplates instance with initial field values.
        The creator id is the openstack user id of the authenticated user. The
        AppTemplate is automatically added to favorites.

        :param AppTemplateSerializer serializer: Serializer for the AppTemplates model
        :return: None
        :rtype: None
        """
        serializer.save(creator_id=self.request.myuser, approved=False)
        # Create a favorite item of the newly created AppTemplate
        Favorites.objects.create(app_template_id=serializer.instance, user_id=self.request.myuser)

    @override
    def get_queryset(self) -> QuerySet[AppTemplates]:
        """
        Retrieve the queryset of AppTemplates,
        optionally filtered by search, public, and approved status.
        The scope of retrieved AppTemplates depends on the access level of the user.

        :return: Filtered queryset of AppTemplates
        :rtype: QuerySet
        """
        user = self.request.myuser
        user_access_level = user.role_id.access_level

        # Only consider AppTemplates that are not deleted
        queryset = AppTemplates.objects.filter(deleted=False)

        if user_access_level >= REQUIRED_ACCESS_LEVELS[('app-template-list-all', 'GET')]:
            # Users with sufficient access level can see their own AppTemplates
            # and all public (including not approved AppTemplates
            queryset = (queryset.filter(creator_id=user)
                        | queryset.filter(public=True))
        else:
            # Normal Users can only see public and approved AppTemplates plus own AppTemplates
            queryset = (queryset.filter(creator_id=user)
                        | queryset.filter(public=True, approved=True))

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
                Q(id__icontains=search)
            )

        # Filter
        if public is not None:
            queryset = queryset.filter(public=public)
        if approved is not None:
            queryset = queryset.filter(approved=approved)

        return queryset

    @action(detail=True, methods=['patch'])
    def approve(self, request, pk=None) -> Response:
        """
        Approve an AppTemplate to make it public and accessible for others.

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

    @action(detail=True, methods=['patch'])
    def reject(self, request, pk=None) -> Response:
        """
        Reject an AppTemplate. Sets public and approved to
        false making the AppTemplate only visible for the creator.

        :param Request request: The HTTP request object
        :return: HTTP response with the approval status
        :rtype: Response
        """
        app_template_id = self.get_object().id
        app_template = reject_app_template(app_template_id)
        return Response(
            {"id": app_template.id, "public": app_template.public, "approved": app_template.approved},
            status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='name/(?P<name>[^/.]+)\\/collisions',
            name='check-name-collisions')
    def check_name_collisions(self, request, name=None) -> Response:
        """
        Check for name collisions in AppTemplates.

        :param Request request: The HTTP request object
        :param str name: Name to check for collisions
        :return: HTTP response with collision status
        :rtype: Response
        """
        collisions = check_app_template_name_collisions(name)

        response_object = {"name": name, "collisions": collisions}
        return Response(response_object, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path='favorites')
    def favorites(self, request) -> Response:
        """
        Lists all AppTemplate which are favorites of the current user.

        :param Request request: The HTTP request object
        :return: HTTP response with the list of favorite AppTemplates
        :rtype: Response
        """
        user = request.myuser
        favorites_app_template_ids = (Favorites.objects.filter(user_id=user)
                                      .values_list('app_template_id', flat=True))

        # Filter for the list of app_template_ids
        app_templates = AppTemplates.objects.filter(id__in=favorites_app_template_ids)

        serializer = AppTemplateSerializer(app_templates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FavoritesViewSet(viewsets.ModelViewSet):
    serializer_class = FavoritesSerializer

    def get_queryset(self) ->QuerySet[Favorites]:
        """
        retrieve the queryset of Favorites. Each User can only access own favorites

        :return: queryset of Favorites
        :rtype: Favorites
        """

        user = self.request.myuser
        queryset = Favorites.objects.filter(user_id=user)
        return queryset

    def perform_create(self, serializer) ->None:
        """
        Adds AppTemplate to Favorites of current User

        :param FavoritesSerializer serializer: Serializer for the Favorites model
        :return: None
        :rtype: None
        """
        serializer.save(user_id=self.request.myuser)

    @action(detail=False, methods=['DELETE'], url_path='delete_by_app_template')
    def delete_by_app_template(self, request) ->Response:
        app_template_id = request.data.get('app_template_id')
        user_id = request.myuser
        try:
            favorite = Favorites.objects.get(app_template_id=app_template_id, user_id=user_id)
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Favorites.DoesNotExist:
            logger.info(f"Favorite for AppTemplate {app_template_id} not found")
            return Response({"detail": "Favorite not found."}, status=status.HTTP_404_NOT_FOUND)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling Users model operations.

    This ViewSet provides default CRUD operations for the Users model.

    :param serializer_class: Serializer class for Users model
    """
    serializer_class = UserSerializer

    @override
    def get_queryset(self) -> QuerySet[Users]:
        """
        Retrieve queryset of Users.
        The scope of retrieved Users depends on the access level of the user.

        :return: queryset of Users
        :rtype: QuerySet
        """
        user = self.request.myuser
        user_access_level = user.role_id.access_level

        # Only consider Users that are not deleted
        queryset = Users.objects.filter(deleted=False)

        if user_access_level < REQUIRED_ACCESS_LEVELS[('user-list', 'GET')]:
            # Users with insufficient access level can only see themselves
            queryset = queryset.filter(id=user)

        return queryset

class RoleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling Roles model operations.

    This ViewSet provides default CRUD operations for the Roles model.

    :param queryset: Queryset of all Roles instances
    :param serializer_class: Serializer class for Roles model
    """
    queryset = Roles.objects.all()
    serializer_class = RoleSerializer
