
from django.db import models
from django.core.exceptions import ValidationError
from hospitals.models import HospitalProfile


class BloodInventory(models.Model):

    class BloodGroup(models.TextChoices):
        A_POSITIVE = "A+", "A Positive"
        A_NEGATIVE = "A-", "A Negative"
        B_POSITIVE = "B+", "B Positive"
        B_NEGATIVE = "B-", "B Negative"
        AB_POSITIVE = "AB+", "AB Positive"
        AB_NEGATIVE = "AB-", "AB Negative"
        O_POSITIVE = "O+", "O Positive"
        O_NEGATIVE = "O-", "O Negative"

    class Component(models.TextChoices):
        WHOLE_BLOOD = "WHOLE_BLOOD", "Whole Blood"
        RED_CELLS = "RED_CELLS", "Red Blood Cells"
        PLASMA = "PLASMA", "Plasma"
        PLATELETS = "PLATELETS", "Platelets"
        CRYOPRECIPITATE = "CRYOPRECIPITATE", "Cryoprecipitate"

    class TestingStatus(models.TextChoices):
        PENDING = "PENDING", "Testing Pending"
        CLEARED = "CLEARED", "Testing Cleared"
        REACTIVE = "REACTIVE", "Reactive"

    class InventoryStatus(models.TextChoices):
        QUARANTINED = "QUARANTINED", "Quarantined"
        AVAILABLE = "AVAILABLE", "Available"
        DISCARDED = "DISCARDED", "Discarded"

    hospital = models.ForeignKey(
        HospitalProfile,
        on_delete=models.PROTECT,
        related_name="blood_inventory"
    )

    blood_group = models.CharField(
        max_length=3,
        choices=BloodGroup.choices
    )

    component = models.CharField(
        max_length=20,
        choices=Component.choices
    )

    batch_number = models.CharField(
        max_length=100,
        unique=True
    )

    units_available = models.PositiveIntegerField(default=0)

    collection_date = models.DateField()
    expiry_date = models.DateField()

    testing_status = models.CharField(
        max_length=20,
        choices=TestingStatus.choices,
        default=TestingStatus.PENDING
    )

    inventory_status = models.CharField(
        max_length=20,
        choices=InventoryStatus.choices,
        default=InventoryStatus.QUARANTINED
    )

    storage_location = models.CharField(
        max_length=150,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()

        if self.expiry_date and self.collection_date:
            if self.expiry_date <= self.collection_date:
                raise ValidationError({
                    "expiry_date": "Expiry date must be after collection date."
                })

    def __str__(self):
        return (
            f"{self.batch_number} - "
            f"{self.blood_group} - {self.component}"
        )
