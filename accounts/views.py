
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse

from .models import User
from .forms import IndividualRegistrationForm


def register(request):
    if request.method == "POST":
        form = IndividualRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            messages.success(
                request,
                "Your LifeLink account has been created successfully!"
            )
            return redirect("login")
    else:
        form = IndividualRegistrationForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form}
    )


class RoleBasedLoginView(LoginView):
    template_name = "accounts/login.html"

    def get_default_redirect_url(self):

        if self.request.user.role == User.Role.ADMIN:
            if self.request.user.is_staff:
                return reverse("admin_dashboard")

        if self.request.user.role == User.Role.HOSPITAL:
            return reverse("hospital_dashboard")

        return reverse("dashboard")


@login_required
def dashboard(request):

    if request.user.role != User.Role.INDIVIDUAL:
        messages.error(
            request,
            "You are not authorized to access this dashboard."
        )
        return redirect("home")

    return render(
        request,
        "accounts/dashboard.html"
    )
