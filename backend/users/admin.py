from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User, Subscription


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Админка для пользователей."""
    list_display = (
        'id', 'username', 'email', 'first_name', 'last_name', 'is_staff'
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {
            'fields': ('first_name', 'last_name', 'email', 'avatar')
        }),
        ('Права доступа', {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
        ('Важные даты', {
            'fields': ('last_login', 'date_joined')
        }),
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Админка для подписок."""
    list_display = ('id', 'user', 'author', 'created')
    list_filter = ('user', 'author')
    search_fields = ('user__username', 'author__username')