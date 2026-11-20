from django.contrib import admin
from .models import BloodInventory


@admin.register(BloodInventory)
class BloodInventoryAdmin(admin.ModelAdmin):

    list_display = (
        'batch_number',
        'hospital',
        'blood_group',
        'component',
        'units_available',
        'collection_date',
        'expiry_date',
        'testing_status',
        'inventory_status',
    )

    list_filter = (
        'blood_group',
        'component',
        'testing_status',
        'inventory_status',
        'hospital',
    )

    search_fields = (
        'batch_number',
        'hospital__hospital_name',
        'storage_location',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    date_hierarchy = 'collection_date'
