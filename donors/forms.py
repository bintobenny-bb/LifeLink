from django import forms
from .models import DonorProfile


class DonorProfileForm(forms.ModelForm):

    class Meta:
        model = DonorProfile
        exclude = ["user", "created_at", "updated_at"]

        widgets = {
            "date_of_birth": forms.DateInput(
                attrs={"type": "date"}
            ),
            "address": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Enter your full address"}
            ),
        }
