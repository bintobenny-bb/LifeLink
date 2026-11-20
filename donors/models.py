
from django.conf import settings
from django.db import models


class DonorProfile(models.Model):

    class BloodGroup(models.TextChoices):
        A_POSITIVE = "A+", "A Positive"
        A_NEGATIVE = "A-", "A Negative"
        B_POSITIVE = "B+", "B Positive"
        B_NEGATIVE = "B-", "B Negative"
        AB_POSITIVE = "AB+", "AB Positive"
        AB_NEGATIVE = "AB-", "AB Negative"
        O_POSITIVE = "O+", "O Positive"
        O_NEGATIVE = "O-", "O Negative"

    class Gender(models.TextChoices):
        MALE = "MALE", "Male"
        FEMALE = "FEMALE", "Female"
        OTHER = "OTHER", "Other"
        PREFER_NOT_TO_SAY = "PREFER_NOT_TO_SAY", "Prefer not to say"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="donor_profile"
    )

    date_of_birth = models.DateField()
    gender = models.CharField(
        max_length=20,
        choices=Gender.choices
    )

    blood_group = models.CharField(
        max_length=3,
        choices=BloodGroup.choices
    )

    address = models.TextField()
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)

    is_available = models.BooleanField(default=False)

    contact_consent = models.BooleanField(default=False)
    location_sharing_consent = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.blood_group}"
