from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Favorite, Subscription

User = get_user_model()


class FavoriteAdmin(admin.ModelAdmin):
    model = Favorite
    list_display = ('user', 'recipe')


class SubscriptionAdmin(admin.ModelAdmin):
    model = Subscription
    list_display = ('user', 'author')


class UserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'username', 'is_staff', 'is_active',)
    list_filter = ('email', 'username', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Description', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2', 'is_staff', 'is_active'
            )
        }),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)


admin.site.unregister(User)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(User, UserAdmin)
