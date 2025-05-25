from django.db import models

from apps.users.models import User


class Device(models.Model):
    device_id = models.CharField(max_length=100, unique=True)
    assigned_user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.device_id


class LocationPing(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='location_ping')
    latitude = models.FloatField()
    longitude = models.FloatField()
    ping_time = models.DateTimeField()

    class Meta:
        ordering = ['-ping_time']
