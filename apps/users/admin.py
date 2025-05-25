from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'is_staff', 'is_active')
    search_fields = ('id', 'username')
    ordering = ('id',)
