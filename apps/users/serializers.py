from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'name']

    def get_name(self, obj):
        return obj.username