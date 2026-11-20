
from django.conf import settings
from django.db import models


class HospitalProfile(models.Model):

    class HospitalType(models.TextChoices):
        GOVERNMENT = "GOVERNMENT", "Government"
        PRIVATE = "PRIVATE", "Private"
        CHARITABLE = "CHARITABLE", "Charitable"
        OTHER = "OTHER", "Other"

    class VerificationStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        VERIFIED = "VERIFIED", "Verified"
        REJECTED = "REJECTED", "Rejected"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="hospital_profile"
    )

    hospital_name = models.CharField(max_length=200)
    registration_number = models.CharField(
        max_length=100,
        unique=True
    )

    hospital_type = models.CharField(
        max_length=20,
        choices=HospitalType.choices
    )

    contact_person = models.CharField(max_length=150)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)

    address = models.TextField()
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)

    verification_status = models.CharField(
        max_length=20,
        choices=VerificationStatus.choices,
        default=VerificationStatus.PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.hospital_name
