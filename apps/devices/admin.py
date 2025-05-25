from django.contrib import admin

from .models import Device, LocationPing


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'assigned_user')

@admin.register(LocationPing)
class LocationPingAdmin(admin.ModelAdmin):
    list_display = ('device', 'latitude', 'longitude', 'ping_time')
