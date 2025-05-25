from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import User
from apps.devices.models import Device
from apps.devices import serializers as device_serializers


tag = "/users"


class UserLastLocationView(APIView):
    @swagger_auto_schema(
        operation_description="Get the last known location for the user's assigned device.",
        tags=[tag],
        responses={
            200: openapi.Response(
                description="Last known location.",
                schema=device_serializers.LastLocationSerializer
            ),
            404: openapi.Response(description="User, device, or location not found."),
            500: openapi.Response(description="Internal server error.")
        }
    )
    def get(self, request, id):
        user = get_object_or_404(User, pk=id)
        device = Device.objects.filter(assigned_user=user).first()
        if not device:
            return Response({'error': 'No assigned device'}, status=status.HTTP_404_NOT_FOUND)

        location = device.location_ping.first()
        if not location:
            return Response({'error': 'No location found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = device_serializers.LastLocationSerializer(location)
        return Response(serializer.data)

