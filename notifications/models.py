
from django.conf import settings
from django.db import models
from requests_app.models import BloodRequest


class Notification(models.Model):

    class NotificationType(models.TextChoices):
        BLOOD_REQUEST = "BLOOD_REQUEST", "Blood Request"
        EMERGENCY = "EMERGENCY", "Emergency Alert"
        REQUEST_UPDATE = "REQUEST_UPDATE", "Request Update"
        DONOR_ALERT = "DONOR_ALERT", "Donor Alert"
        DONATION_REMINDER = "DONATION_REMINDER", "Donation Reminder"
        SYSTEM = "SYSTEM", "System Notification"

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    notification_type = models.CharField(
        max_length=25,
        choices=NotificationType.choices,
        default=NotificationType.SYSTEM
    )

    title = models.CharField(max_length=200)
    message = models.TextField()

    related_request = models.ForeignKey(
        BloodRequest,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="notifications"
    )

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.recipient.username}"
