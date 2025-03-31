
import logging
from django.db.models import Q, QuerySet
from django.core.exceptions import ObjectDoesNotExist
from typing_extensions import override
from rest_framework.request import Request

from eduvmstore.api.serializers import (AppTemplateSerializer, FavoritesSerializer,
                                        UserSerializer, RoleSerializer)
from eduvmstore.db.models import AppTemplates, Favorites, Users, Roles
from eduvmstore.config.access_levels import REQUIRED_ACCESS_LEVELS
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from eduvmstore.db.operations.app_templates import (approve_app_template,
                                                    check_current_name_collision,
                                                    reject_app_template, has_version_suffix,
                                                    extract_version_suffix)
from eduvmstore.utils.access_control import has_access_level

logger = logging.getLogger('eduvmstore_logger')
class AppTemplateViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling AppTemplate model operations.

    This ViewSet provides default CRUD operations for the AppTemplates model,
    including custom actions for approving templates and checking for a name collision.

    :param serializer_class: Serializer class for AppTemplates model
    """
    serializer_class = AppTemplateSerializer

    @override
    def perform_create(self, serializer: AppTemplateSerializer) -> None:
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

        # Only consider AppTemplates that are not deleted
        queryset = AppTemplates.objects.filter(deleted=False)

        if has_access_level(user, 'app-template-list-all', 'GET'):
            # Users with sufficient access level can see their own AppTemplates
            # and all public (including not approved AppTemplates
            queryset = queryset.filter(Q(creator_id=user) | Q(public=True))
        else:
            # Normal Users can only see public and approved AppTemplates plus own AppTemplates
            queryset = queryset.filter(Q(creator_id=user) | Q(public=True, approved=True))

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
    def approve(self, request: Request, pk: str=None) -> Response:
        """
        Approve an AppTemplate to make it public and accessible for others.

        :param Request request: The HTTP request object
        :param str pk: Primary key of the AppTemplate to approve
        :return: HTTP response with the approval status
        :rtype: Response
        """
        original_app_template_id = self.get_object().id
        public_app_template = approve_app_template(original_app_template_id)
        return Response(
            {
                "original_app_template": {
                    "id": original_app_template_id
                    },
                "public_app_template": {
                    "id": public_app_template.id,
                    "approved": public_app_template.approved
                }
            }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def reject(self, request: Request, pk: str=None) -> Response:
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

    @action(detail=False, methods=['get'], url_path='name/(?P<name>[^/.]+)\\/collision',
            name='check-name-collision')
    def check_name_collision(self, request: Request, name: str=None) -> Response:
        """
        Check for a name collision with existing and future AppTemplates.

        :param Request request: The HTTP request object
        :param str name: Name to check for a collision
        :return: HTTP response with collision status
        :rtype: Response
        """
        current_collision = check_current_name_collision(name)

        potential_future_collision = has_version_suffix(name)

        reason = "No collision found."
        if current_collision:
            reason = "AppTemplate with this name already exists"
        elif potential_future_collision:
            suffix = extract_version_suffix(name)
            reason = (f"Suffix '{suffix}' is not allowed in the name "
                      "to prevent future collisions with approved AppTemplates")

        response_object = {"name": name,
                           "collision": current_collision or potential_future_collision,
                           "reason": reason}
        return Response(response_object, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path='favorites')
    def favorites(self, request: Request) -> Response:
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
        app_templates = self.get_queryset().filter(id__in=favorites_app_template_ids)

        serializer = AppTemplateSerializer(app_templates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @override
    def destroy(self, request: Request, *args, **kwargs) -> Response:
        """
        Delete an AppTemplate.
        Only allows deletion of approved AppTemplates
        if the user has the required access level.

        :param Request request: The HTTP request object
        :return: HTTP response with the deletion status
        :rtype: Response
        """
        app_template = self.get_object()
        user = request.myuser
        if (app_template.approved and
                not has_access_level(user, 'app-template-delete-approved', 'DELETE')):
            return Response(
                {'error': f'Access level of user {user.id} not sufficient'
                          f' to delete approved AppTemplates'}, status=403)

        # Proceed with standard deletion
        return super().destroy(request, *args, **kwargs)

class FavoritesViewSet(viewsets.ModelViewSet):
    serializer_class = FavoritesSerializer

    def get_queryset(self) -> QuerySet[Favorites]:
        """
        retrieve the queryset of Favorites. Each User can only access own favorites

        :return: queryset of Favorites
        :rtype: QuerySet
        """

        user = self.request.myuser
        queryset = Favorites.objects.filter(user_id=user)
        return queryset

    def perform_create(self, serializer: FavoritesSerializer) -> None:
        """
        Adds AppTemplate to Favorites of current User

        :param FavoritesSerializer serializer: Serializer for the Favorites model
        :return: None
        :rtype: None
        """
        serializer.save(user_id=self.request.myuser)

    @action(detail=False, methods=['DELETE'], url_path='delete_by_app_template')
    def delete_by_app_template(self, request: Request) -> Response:
        app_template_id = request.data.get('app_template_id')
        user_id = request.myuser
        try:
            favorite = Favorites.objects.get(app_template_id=app_template_id, user_id=user_id)
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Favorites.ObjectDoesNotExist:
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
