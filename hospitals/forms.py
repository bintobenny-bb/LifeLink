
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import HospitalProfile

User = get_user_model()


class HospitalRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ["username", "email", "phone_number"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.HOSPITAL

        if commit:
            user.save()

        return user


class HospitalProfileForm(forms.ModelForm):

    latitude = forms.DecimalField(
        min_value=-90,
        max_value=90,
        widget=forms.HiddenInput()
    )

    longitude = forms.DecimalField(
        min_value=-180,
        max_value=180,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = HospitalProfile
        exclude = [
            "user",
            "verification_status",
            "created_at",
            "updated_at"
        ]

    def clean_registration_certificate(self):
        certificate = self.cleaned_data.get("registration_certificate")

        if certificate:
            allowed_extensions = [".pdf", ".jpg", ".jpeg", ".png"]
            extension = certificate.name.lower().rsplit(".", 1)[-1]

            if f".{extension}" not in allowed_extensions:
                raise forms.ValidationError(
                    "Only PDF, JPG, JPEG and PNG files are allowed."
                )

            if certificate.size > 5 * 1024 * 1024:
                raise forms.ValidationError(
                    "Certificate size must not exceed 5 MB."
                )

        return certificate

    def clean(self):
        cleaned_data = super().clean()

        latitude = cleaned_data.get("latitude")
        longitude = cleaned_data.get("longitude")

        if latitude is None or longitude is None:
            raise forms.ValidationError(
                "Please select your hospital location on the map."
            )

        return cleaned_data
