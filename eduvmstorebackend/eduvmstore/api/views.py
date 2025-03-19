
import logging
from django.db.models import Q, QuerySet
from django.core.exceptions import ObjectDoesNotExist
from typing_extensions import override

from eduvmstore.config.access_levels import REQUIRED_ACCESS_LEVELS
from eduvmstore.api.serializers import AppTemplateSerializer, RoleSerializer, UserSerializer
from eduvmstore.db.models import AppTemplates, Roles, Users
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from eduvmstore.db.operations.app_templates import (create_app_template,
                                                    list_app_templates,
                                                    approve_app_template,
                                                    check_app_template_name_collisions,
                                                    soft_delete_app_template, reject_app_template)
from eduvmstore.db.operations.users import get_user_by_id, soft_delete_user


# from eduvmstore.db.operations.app_templates import create_app_template, list_app_templates


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
        Custom handle creation of an AppTemplates instance with initial field values.

        :param AppTemplateSerializer serializer: Serializer for the AppTemplates model
        :return: None
        :rtype: None
        """
        serializer.save(creator_id=self.request.myuser, approved=False)
        # creator_id: Ensures that the creator_id is set to the ID of the authenticated user

    @override
    def get_queryset(self) -> QuerySet[AppTemplates]:
        """
        Custom retrieval of the queryset of AppTemplates,
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

    @action(detail=True, methods=['patch'])
    def reject(self, request, pk=None) -> Response:
        """
        Custom endpoint to reject an AppTemplate. Sets public and approved to
        false making the AppTemplate only visible for the creator.

        :param Request request: The HTTP request object
        :param str pk: Primary key of the AppTemplate to approve
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
        Custom endpoint to check for name collisions in AppTemplates.

        :param Request request: The HTTP request object
        :param str name: Name to check for collisions
        :return: HTTP response with collision status
        :rtype: Response
        """
        collisions = check_app_template_name_collisions(name)

        response_object = {"name": name, "collisions": collisions}
        return Response(response_object, status=status.HTTP_200_OK)

    @override
    def perform_destroy(self, instance) -> Response:
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

    :param serializer_class: Serializer class for Users model
    """
    serializer_class = UserSerializer

    def retrieve(self, request, pk=None) -> Response:
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

    @override
    def get_queryset(self) -> QuerySet[Users]:
        """
        Custom retrieval of the queryset of Users.
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

    @override
    def perform_destroy(self, instance) -> Response:
        """
        Soft delete a User by marking them as deleted.

        :param Users instance: The User instance to delete
        :return: HTTP response with no content
        :rtype: Response
        """
        soft_delete_user(self.get_object().id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RoleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling Roles model operations.

    This ViewSet provides default CRUD operations for the Roles model.

    :param queryset: Queryset of all Roles instances
    :param serializer_class: Serializer class for Roles model
    """
    queryset = Roles.objects.all()
    serializer_class = RoleSerializer
