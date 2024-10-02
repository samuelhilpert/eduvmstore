from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from eduvmstorebackend.eduvmstore.services.nova_service import list_instances, create_instance
from eduvmstorebackend.eduvmstore.services.glance_service import list_images
from eduvmstorebackend.eduvmstore.api.serializers import AppTemplateSerializer
from eduvmstorebackend.eduvmstore.db.models import AppTemplate
from eduvmstorebackend.eduvmstore.db.session import get_db


class AppTemplateViewSet(viewsets.ViewSet):

    def list(self, request):
        db = next(get_db())
        templates = db.query(AppTemplate).all()
        return Response([template.name for template in templates])

    def create(self, request):
        db = next(get_db())
        data = request.data
        new_template = AppTemplate(
            name=data['name'],
            description=data['description'],
            image_id=data['image_id'],
            visibility=data['visibility']
        )
        db.add(new_template)
        db.commit()
        return Response(status=status.HTTP_201_CREATED)

class InstanceListAPI(APIView):
    """API to list OpenStack instances."""
    def get(self, request):
        instances = list_instances()
        return Response({'instances': instances}, status=status.HTTP_200_OK)

class ImageListAPI(APIView):
    """API to list OpenStack images."""
    def get(self, request):
        images = list_images()
        return Response({'images': images}, status=status.HTTP_200_OK)