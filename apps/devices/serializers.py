from rest_framework import serializers

from .models import Device, LocationPing


class AssignDeviceSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationPing
        fields = ['latitude', 'longitude', 'ping_time']


class LastLocationSerializer(serializers.ModelSerializer):
    timestamp = serializers.SerializerMethodField()

    class Meta:
        model = LocationPing
        fields = ['latitude', 'longitude', 'timestamp']
    
    def get_timestamp(self, obj):
        return obj.ping_time


class DeviceStatusSerializer(serializers.ModelSerializer):
    is_assigned = serializers.SerializerMethodField()

    class Meta:
        model = Device
        fields = ['device_id', 'is_assigned']

    def get_is_assigned(self, obj):
        return obj.assigned_user is not None

