from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = (
        'email', 'login', 'is_staff', 'is_active'
    )
    list_filter = (
        'email', 'login'
    )
