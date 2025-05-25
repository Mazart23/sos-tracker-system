from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import Device, LocationPing
from apps.users.models import User
from sos_system.general import serializers as general_serializers
from . import serializers


tag = "/devices"


class AssignDeviceView(APIView):
    @swagger_auto_schema(
        operation_description="""
        Assign a user to a device. 
        If the user is already assigned to another device, it will be unassigned first.
        """,
        request_body=serializers.AssignDeviceSerializer,
        tags=[tag],
        responses={
            200: openapi.Response(
                description="Device successfully assigned.",
                schema=general_serializers.StatusSerializer
            ),
            400: openapi.Response(description="Validation error."),
            404: openapi.Response(description="Device or user not found."),
            500: openapi.Response(description="Internal server error.")
        }
    )
    def post(self, request, id):
        device = get_object_or_404(Device, device_id=id)

        serializer = serializers.AssignDeviceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(User, pk=serializer.validated_data['user_id'])

        if device.assigned_user:
            device.assigned_user = None

        Device.objects.filter(assigned_user=user).update(assigned_user=None)

        device.assigned_user = user
        device.save()
        return Response({'status': 'assigned'})


class PingLocationView(APIView):
    @swagger_auto_schema(
        operation_description="Submit a GPS ping (location) for a device. The device must be assigned to only one user at a time.",
        request_body=serializers.LocationSerializer,
        tags=[tag],
        responses={
            200: openapi.Response(
                description="Location successfully recorded.",
                schema=general_serializers.StatusSerializer
            ),
            400: openapi.Response(description="Validation error or unassigned device."),
            404: openapi.Response(description="Device not found."),
            500: openapi.Response(description="Internal server error.")
        }
    )
    def post(self, request, id):
        device = get_object_or_404(Device, device_id=id)

        if not device.assigned_user:
            return Response({'error': 'Device already not assigned'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.LocationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        LocationPing.objects.create(device=device, **serializer.validated_data)
        return Response({'status': 'location recorded'})


class ListDevicesView(APIView):
    @swagger_auto_schema(
        operation_description="Return a list of all devices and their current assignment status.",
        tags=[tag],
        responses={
            200: openapi.Response(
                description="List of devices", 
                schema=serializers.DeviceStatusSerializer(many=True)
            ),
            500: openapi.Response(description="Internal server error.")
        }
    )
    def get(self, request):
        devices = Device.objects.all()
        serializer = serializers.DeviceStatusSerializer(devices, many=True)
        return Response(serializer.data)


class UnassignDeviceView(APIView):
    @swagger_auto_schema(
        operation_description="Unassign a user from the given device.",
        tags=[tag],
        responses={
            200: openapi.Response(
                description="Device unassigned.",
                schema=general_serializers.StatusSerializer
            ),
            404: openapi.Response(description="Device not found."),
            500: openapi.Response(description="Internal server error.")
        }
    )
    def post(self, request, id):
        device = get_object_or_404(Device, device_id=id)

        if not device.assigned_user:
            return Response({'error': 'Device not assigned'}, status=status.HTTP_400_BAD_REQUEST)
        
        device.assigned_user = None
        device.save()
        return Response({'status': 'unassigned'})
