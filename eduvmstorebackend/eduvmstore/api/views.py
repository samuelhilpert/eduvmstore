from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from eduvmstore.services.nova_service import create_instance
from eduvmstore.services.glance_service import list_images
from eduvmstore.api.serializers import AppTemplateSerializer
from eduvmstore.db.models import AppTemplate
from eduvmstore.db.session import get_db
from eduvmstore.db.db_operations import create_app_template
from eduvmstore.db.models import User



class TestAPI(APIView):
    def get(self, request):
        return Response({'status': 'ok'})

class AppTemplateViewSet(viewsets.ViewSet):

    def list(self, request):
        db = next(get_db())
        templates = db.query(AppTemplate).all()
        return Response([template.name for template in templates])

    def create(self, request):
        db = next(get_db())  # Get the database session
        data = request.data

        try:
            # Prepare the data for the template creation
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

            # Call the create_app_template method from db_operations
            new_template = create_app_template(db, template_data)

            # Serialize the result (assuming you have a serializer for AppTemplate)
            serializer = AppTemplateSerializer(new_template)  # Adjust serializer as needed

            # Return the created template data with a 201 status
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