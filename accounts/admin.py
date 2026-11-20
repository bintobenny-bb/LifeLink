from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        'username',
        'email',
        'role',
        'phone_number',
        'is_active',
        'is_staff'
    )

    list_filter = (
        'role',
        'is_active',
        'is_staff'
    )

    search_fields = (
        'username',
        'email',
        'phone_number'
    )

    fieldsets = UserAdmin.fieldsets + (
        ('LifeLink Information', {
            'fields': (
                'role',
                'phone_number',
            )
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('LifeLink Information', {
            'fields': (
                'email',
                'role',
                'phone_number',
            )
        }),
    )
