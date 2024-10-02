from django.shortcuts import render

# app_name/views.py
from rest_framework import viewsets
from eduvmstorebackend.eduvmstore.serializers import AppTemplateSerializer
from eduvmstorebackend.eduvmstore.db.models import AppTemplate
from eduvmstorebackend.eduvmstore.db import get_db


class AppTemplateViewSet(viewsets.ViewSet):

    def list(self, request):
        db = next(get_db())
        templates = db.query(AppTemplate).all()
        serializer = AppTemplateSerializer(templates, many=True)
        return Response(serializer.data)

    def create(self, request):
        db = next(get_db())
        serializer = AppTemplateSerializer(data=request.data)
        if serializer.is_valid():
            app_template = AppTemplate(**serializer.validated_data)
            db.add(app_template)
            db.commit()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
