from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from eduvmstore.services.glance_service import list_images
from eduvmstore.api.serializers import AppTemplateSerializer
from eduvmstore.db.operations.app_templates import create_app_template, list_app_templates

class TestAPI(APIView):
    def get(self, request):
        return Response({'status': 'ok'})

class AppTemplateViewSet(viewsets.ViewSet):

    def list(self, request):
        templates = list_app_templates()
        serializer = AppTemplateSerializer(templates, many=True)
        return Response({
            "data": serializer.data,
            "message": "AppTemplates queried"
        }, status=status.HTTP_200_OK)

    def create(self, request):
        try:
            template = create_app_template(request.data)
            serializer = AppTemplateSerializer(template)
            return Response({
                "data": serializer.data,
                "message": "AppTemplate created"
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


    # def create(self, request):
    #     data = request.data
    #
    #     try:
    #         app_template_data = {
    #             'name': data['name'],
    #             'description': data['description'],
    #             'short_description': data['short_description'],
    #             'instantiation_notice': data.get('instantiation_notice'),
    #             'image_id': data['image_id'],
    #             'creator_id': data.get('creator_id'),
    #             'version': data.get('version', '1.0'),  # Default to '1.0'
    #             'public': data.get('public', False),
    #             'approved': data.get('approved', False),
    #             'fixed_ram_gb': data['fixed_ram_gb'],
    #             'fixed_disk_gb': data['fixed_disk_gb'],
    #             'fixed_cores': data['fixed_cores'],
    #             'per_user_ram_gb': data['per_user_ram_gb'],
    #             'per_user_disk_gb': data['per_user_disk_gb'],
    #             'per_user_cores': data['per_user_cores']
    #         }
    #
    #         new_app_template = create_app_template(app_template_data)
    #         serializer = AppTemplateSerializer(new_app_template)
    #         return Response(status=status.HTTP_201_CREATED)
    #
    #     except Exception as e:
    #         return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    def list(self, request):
        return Response({'status': 'ok'})


class ImageListAPI(APIView):
    """API to list OpenStack images."""
    def get(self, request):
        return Response(status=status.HTTP_200_OK)