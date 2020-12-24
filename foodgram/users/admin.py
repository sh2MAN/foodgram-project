from django.contrib import admin

from .models import Favorite, Subscription, User


class FavoriteAdmin(admin.ModelAdmin):
    model = Favorite
    list_display = ('user__username', 'recipe__title')


class SubscriptionAdmin(admin.ModelAdmin):
    model = Subscription
    list_display = ('user__username', 'author__username')


class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('email', 'username', 'is_staff', 'is_active')
    list_filter = ('email', 'username')


admin.site.unregister(User)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(User, UserAdmin)
