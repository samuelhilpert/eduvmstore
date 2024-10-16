from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView

# from eduvmstore.services.glance_service import list_images
from eduvmstore.api.serializers import AppTemplateSerializer, UserSerializer, RoleSerializer
from eduvmstore.db.models import AppTemplate, User, Role
from eduvmstore.db.operations.app_templates import create_app_template, list_app_templates


class TestAPI(APIView):
    def get(self, request):
        return Response({'status': 'ok'})

class AppTemplateViewSet(viewsets.ModelViewSet):
    queryset = AppTemplate.objects.filter(deleted=False)
    serializer_class = AppTemplateSerializer

    # def perform_create(self, serializer):
    #     # Setzt das Feld 'creator_id' auf die ID des aktuell authentifizierten Benutzers
    #     serializer.save(creator_id=self.request.user.id)

    def get_queryset(self):
        queryset = AppTemplate.objects.all()
        # Optional: Filter basierend auf Query-Parametern
        public = self.request.query_params.get('public', None)
        approved = self.request.query_params.get('approved', None)
        if public is not None:
            queryset = queryset.filter(public=public)
        if approved is not None:
            queryset = queryset.filter(approved=approved)
        return queryset

    @action(detail=True, methods=['patch'])
    def approve(self, request, pk=None):
        # Benutzerdefinierte Aktion zum Genehmigen eines AppTemplates
        app_template = self.get_object()
        app_template.approved = True
        app_template.save()
        return Response(
            {"data": {"id": app_template.id, "approved": app_template.approved}, "message": "AppTemplate approved"},
            status=status.HTTP_200_OK)

    # def list(self, request):
    #     templates = list_app_templates()
    #     serializer = AppTemplateSerializer(templates, many=True)
    #     return Response({"data": serializer.data, "message": "AppTemplates queried"}, status=status.HTTP_200_OK)
    #
    # def create(self, request):
    #     try:
    #         template = create_app_template(request.data)
    #         serializer = AppTemplateSerializer(template)
    #         return Response({"data": serializer.data, "message": "AppTemplate created"}, status=status.HTTP_201_CREATED)
    #     except Exception as e:
    #         return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    #
    # def get(self, request, id):
    #     # Placeholder logic to get details of a specific template
    #     return Response({"data": {}, "message": "AppTemplate found"}, status=status.HTTP_200_OK)
    #
    # def get(self, request):
    #     query = request.GET.get('search', '')
    #     print("query: ",query)
    #     # Placeholder logic for querying templates based on search string
    #     return Response({"data": [], "message": "AppTemplates queried"}, status=status.HTTP_200_OK)
    #
    # def get(self, request):
    #     public = request.GET.get('public')
    #     approved = request.GET.get('approved')
    #     print("public: ",public)
    #     print("apporved: ",approved)
    #     # Placeholder logic for filtering templates based on public and approved status
    #     return Response({"data": [], "message": "AppTemplates queried"}, status=status.HTTP_200_OK)
    #
    # def put(self, request, id):
    #     print("id: ",id)
    #     # Placeholder logic to update an existing template
    #     return Response({"data": {}, "message": "AppTemplate updated"}, status=status.HTTP_200_OK)
    #
    # def delete(self, request, id):
    #     print("id: ",id)
    #     # Placeholder logic to soft delete an AppTemplate
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    #
    # def patch(self, request, id):
    #     # Placeholder logic to approve an AppTemplate for public visibility
    #     return Response({"data": {}, "message": "AppTemplate approved"}, status=status.HTTP_200_OK)
    #
    # def get(self, request, name):
    #     # Placeholder logic to check for naming collisions
    #     return Response({"data": {"collision": False}, "message": "Naming Collisions checked"}, status=status.HTTP_200_OK)

# class UserViewSet(viewsets.ModelViewSet):
#     def list(self, request):
#         # Placeholder logic to list all users
#         return Response({"data": [], "message": "Users queried"}, status=status.HTTP_200_OK)



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(deleted=False)
    serializer_class = UserSerializer


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer




class UserDetailView(APIView):
    def get(self, request, id):
        print("id: ",id)
        # Placeholder logic to get details of a user
        return Response({"data": {}, "message": "User found"}, status=status.HTTP_200_OK)

class UserRoleUpdateView(APIView):
    def patch(self, request, id):
        print("id: ",id)
        # Placeholder logic to update the role of a user
        return Response({"data": {}, "message": "User Role updated"}, status=status.HTTP_200_OK)

class UserDeleteView(APIView):
    def delete(self, request, id):
        # Placeholder logic to soft delete a user
        return Response(status=status.HTTP_204_NO_CONTENT)



class ImageListAPI(APIView):
    """
    API to list OpenStack images.

    """
    def list(self, request):
        return Response(status=status.HTTP_200_OK)

class ImageDetailView(APIView):
    def get(self, request, id):
        print("id: ",id)
        # Placeholder logic to return details of a specific image
        return Response({"data": {}, "message": "Image found"}, status=status.HTTP_200_OK)

class FlavorSelectionView(APIView):
    def post(self, request):
        # Placeholder logic to return possible and best matching flavors
        return Response({"data": {"best_flavor_id": None, "possible_flavor_ids": []}, "message": "Flavors queried"}, status=status.HTTP_200_OK)

class InstanceLaunchView(APIView):
    def post(self, request):
        # Placeholder logic to create an instance
        return Response({"data": {"id": None, "accounts": []}, "message": "Instance created"}, status=status.HTTP_201_CREATED)