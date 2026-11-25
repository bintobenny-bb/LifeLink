from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class IndividualRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "phone_number",
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.INDIVIDUAL

        if commit:
            user.save()

        return user
