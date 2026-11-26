
from django.contrib import admin, messages
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

    fieldsets = (
        ('Hospital Information', {
            'fields': (
                'user',
                'hospital_name',
                'registration_number',
                'hospital_type',
            )
        }),

        ('Contact Information', {
            'fields': (
                'contact_person',
                'contact_email',
                'contact_phone',
            )
        }),

        ('Hospital Address', {
            'fields': (
                'address',
                'city',
                'district',
                'state',
                'postal_code',
            )
        }),

        ('Location Coordinates', {
            'fields': (
                'latitude',
                'longitude',
            )
        }),

        ('Registration Documents', {
            'fields': (
                'registration_certificate',
            )
        }),

        ('Verification', {
            'fields': (
                'verification_status',
            )
        }),

        ('Timestamps', {
            'fields': (
                'created_at',
                'updated_at',
            )
        }),
    )

    actions = [
        'verify_hospitals',
        'reject_hospitals',
    ]

    @admin.action(description="Verify selected hospitals")
    def verify_hospitals(self, request, queryset):
        updated = queryset.update(
            verification_status=HospitalProfile.VerificationStatus.VERIFIED
        )

        self.message_user(
            request,
            f"{updated} hospital(s) successfully verified.",
            messages.SUCCESS
        )

    @admin.action(description="Reject selected hospitals")
    def reject_hospitals(self, request, queryset):
        updated = queryset.update(
            verification_status=HospitalProfile.VerificationStatus.REJECTED
        )

        self.message_user(
            request,
            f"{updated} hospital(s) rejected.",
            messages.WARNING
        )
