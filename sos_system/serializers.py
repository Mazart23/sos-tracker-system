from rest_framework import serializers

from apps.users import serializers as users_serializers


class MapLocationSerializer(serializers.Serializer):
    user = users_serializers.UserSerializer()
    device_id = serializers.CharField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    timestamp = serializers.DateTimeField()