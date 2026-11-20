from django.contrib import admin
from .models import PatientProfile


@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'date_of_birth',
        'gender',
        'city',
        'district',
        'state',
    )

    list_filter = (
        'gender',
        'district',
        'state',
    )

    search_fields = (
        'user__username',
        'user__email',
        'user__phone_number',
        'city',
        'district',
        'emergency_contact_name',
        'emergency_contact_phone',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )
