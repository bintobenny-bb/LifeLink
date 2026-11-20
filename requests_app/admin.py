from django.contrib import admin
from .models import BloodRequest


@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):

    list_display = (
        'request_number',
        'requested_by',
        'patient',
        'requesting_hospital',
        'blood_group',
        'component',
        'units_required',
        'priority',
        'required_by',
        'status',
        'created_at',
    )

    list_filter = (
        'blood_group',
        'component',
        'priority',
        'status',
        'created_at',
    )

    search_fields = (
        'request_number',
        'requested_by__username',
        'requested_by__email',
        'patient__user__username',
        'requesting_hospital__hospital_name',
    )

    readonly_fields = (
        'request_number',
        'created_at',
        'updated_at',
    )

    date_hierarchy = 'created_at'

    ordering = ('-created_at',)
