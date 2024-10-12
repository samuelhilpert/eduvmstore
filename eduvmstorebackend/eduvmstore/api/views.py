from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from eduvmstore.services.glance_service import list_images
from eduvmstore.api.serializers import AppTemplateSerializer
from eduvmstore.db.models import AppTemplate
from eduvmstore.db.session import get_db
from eduvmstore.db.operations.app_templates import create_app_template


class TestAPI(APIView):
    def get(self, request):
        return Response({'status': 'ok'})

class AppTemplateViewSet(viewsets.ViewSet):

    def list(self, request):
        db = next(get_db())
        templates = db.query(AppTemplate).all()
        return Response([{template.name, template.description} for template in templates])
        #return  Response({'templates': AppTemplateSerializer(templates, many=True).data})

    def create(self, request):
        data = request.data
        try:
            template_data = {
                'name': data.get('name'),
                'description': data.get('description'),
                'short_description': data.get('short_description'),
                'instantiation_notice': data.get('instantiation_notice'),
                'image_id': data.get('image_id'),
                'creator_id': data.get('creator_id'),
                'version': data.get('version', '1.0'),  # Default to '1.0'
                'public': data.get('public', False),
                'approved': data.get('approved', False),
                'fixed_ram_gb': data.get('fixed_ram_gb'),
                'fixed_disk_gb': data.get('fixed_disk_gb'),
                'fixed_cores': data.get('fixed_cores'),
                'per_user_ram_gb': data.get('per_user_ram_gb'),
                'per_user_disk_gb': data.get('per_user_disk_gb'),
                'per_user_cores': data.get('per_user_cores')
            }

            new_template = create_app_template(template_data)

            serializer = AppTemplateSerializer(new_template)

            return Response(status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    def list(self, request):
        return Response({'status': 'ok'})


class ImageListAPI(APIView):
    """API to list OpenStack images."""
    def get(self, request):
        images = list_images()
        return Response({'images': images}, status=status.HTTP_200_OK)