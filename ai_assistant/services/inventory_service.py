from django.utils import timezone

from inventory.models import BloodInventory


def get_available_inventory():
    today = timezone.localdate()

    inventory = BloodInventory.objects.filter(
        inventory_status=BloodInventory.InventoryStatus.AVAILABLE,
        testing_status=BloodInventory.TestingStatus.CLEARED,
        expiry_date__gt=today,
        units_available__gt=0
    ).values(
        "blood_group",
        "component",
        "units_available",
        "hospital__hospital_name"
    )

    return list(inventory)
