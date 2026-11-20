
from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

from patients.models import PatientProfile
from hospitals.models import HospitalProfile


class BloodRequest(models.Model):

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

    class Priority(models.TextChoices):
        NORMAL = "NORMAL", "Normal"
        URGENT = "URGENT", "Urgent"
        EMERGENCY = "EMERGENCY", "Emergency"

    class RequestStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        UNDER_REVIEW = "UNDER_REVIEW", "Under Review"
        APPROVED = "APPROVED", "Approved"
        PARTIALLY_FULFILLED = "PARTIALLY_FULFILLED", "Partially Fulfilled"
        FULFILLED = "FULFILLED", "Fulfilled"
        REJECTED = "REJECTED", "Rejected"
        CANCELLED = "CANCELLED", "Cancelled"

    request_number = models.CharField(
        max_length=30,
        unique=True,
        editable=False
    )

    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="blood_requests"
    )

    patient = models.ForeignKey(
        PatientProfile,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="blood_requests"
    )

    requesting_hospital = models.ForeignKey(
        HospitalProfile,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="blood_requests"
    )

    blood_group = models.CharField(
        max_length=3,
        choices=BloodGroup.choices
    )

    component = models.CharField(
        max_length=20,
        choices=Component.choices
    )

    units_required = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    priority = models.CharField(
        max_length=15,
        choices=Priority.choices,
        default=Priority.NORMAL
    )

    required_by = models.DateTimeField()

    reason = models.TextField()

    status = models.CharField(
        max_length=25,
        choices=RequestStatus.choices,
        default=RequestStatus.PENDING
    )

    admin_notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()

        if not self.patient and not self.requesting_hospital:
            raise ValidationError(
                "A patient or requesting hospital must be specified."
            )

        if self.units_required is not None and self.units_required < 1:
            raise ValidationError({
                "units_required": "At least one unit must be requested."
            })

    def save(self, *args, **kwargs):
        if not self.request_number:
            from uuid import uuid4
            self.request_number = f"LL-{uuid4().hex[:12].upper()}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.request_number} - {self.blood_group}"
