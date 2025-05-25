from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from apps.devices.models import Device
from . import serializers


tag = "/"


class MapView(APIView):
    @swagger_auto_schema(
        operation_description="Get a list of all assigned devices with their most recent location and user info.",
        tags=[tag],
        responses={
            200: openapi.Response(
                description="List of devices with ping locations.",
                schema=serializers.MapLocationSerializer(many=True)
            ),
            500: openapi.Response(description="Internal server error.")
        }
    )
    def get(self, request):
        results = []
        devices = Device.objects.exclude(assigned_user=None)

        for device in devices:
            location = device.location_ping.first()
            if location:
                results.append({
                    'user': device.assigned_user,
                    'device_id': device.device_id,
                    'latitude': location.latitude,
                    'longitude': location.longitude,
                    'timestamp': location.ping_time
                })
        
        serializer = serializers.MapLocationSerializer(results, many=True)
        return Response(serializer.data)
