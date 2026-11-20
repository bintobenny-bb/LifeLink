from django.contrib import admin
from .models import DonorProfile


@admin.register(DonorProfile)
class DonorProfileAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'blood_group',
        'gender',
        'city',
        'district',
        'is_available',
        'contact_consent',
        'location_sharing_consent',
    )

    list_filter = (
        'blood_group',
        'gender',
        'is_available',
        'contact_consent',
        'location_sharing_consent',
        'district',
    )

    search_fields = (
        'user__username',
        'user__email',
        'user__phone_number',
        'city',
        'district',
        'blood_group',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )
