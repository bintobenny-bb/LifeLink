
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from accounts.models import User
from .forms import PatientProfileForm


@login_required
def register_patient(request):

    if request.user.role != User.Role.INDIVIDUAL:
        messages.error(
            request, "You are not authorized to register as a patient.")
        return redirect("home")

    if hasattr(request.user, "patient_profile"):
        return redirect("patient_dashboard")

    if request.method == "POST":
        form = PatientProfileForm(request.POST)

        if form.is_valid():
            patient_profile = form.save(commit=False)
            patient_profile.user = request.user
            patient_profile.save()

            messages.success(
                request,
                "Your patient profile has been created successfully!"
            )

            return redirect("patient_dashboard")

    else:
        form = PatientProfileForm()

    return render(
        request,
        "patients/register.html",
        {"form": form}
    )


@login_required
def patient_dashboard(request):

    if request.user.role != User.Role.INDIVIDUAL:
        messages.error(request, "You are not authorized to access this page.")
        return redirect("home")

    if not hasattr(request.user, "patient_profile"):
        return redirect("register_patient")

    return render(
        request,
        "patients/dashboard.html",
        {"patient": request.user.patient_profile}
    )
