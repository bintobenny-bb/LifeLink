from django.contrib import admin
from .models import HospitalProfile


@admin.register(HospitalProfile)
class HospitalProfileAdmin(admin.ModelAdmin):

    list_display = (
        'hospital_name',
        'registration_number',
        'hospital_type',
        'contact_person',
        'city',
        'district',
        'verification_status',
    )

    list_filter = (
        'hospital_type',
        'verification_status',
        'district',
        'state',
    )

    search_fields = (
        'hospital_name',
        'registration_number',
        'contact_person',
        'contact_email',
        'contact_phone',
        'city',
        'district',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )
