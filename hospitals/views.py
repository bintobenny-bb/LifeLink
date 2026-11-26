from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction

from .forms import HospitalRegistrationForm, HospitalProfileForm


def hospital_register(request):

    # Prevent logged-in users from creating another account
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        account_form = HospitalRegistrationForm(request.POST)
        profile_form = HospitalProfileForm(
            request.POST,
            request.FILES
        )

        if account_form.is_valid() and profile_form.is_valid():
            with transaction.atomic():
                user = account_form.save()

                hospital = profile_form.save(commit=False)
                hospital.user = user
                hospital.save()

            messages.success(
                request,
                "Hospital registration submitted successfully. "
                "Your account is awaiting admin verification."
            )
            return redirect("login")

    else:
        account_form = HospitalRegistrationForm()
        profile_form = HospitalProfileForm()

    return render(
        request,
        "hospitals/register.html",
        {
            "account_form": account_form,
            "profile_form": profile_form,
        }
    )


@login_required
def hospital_dashboard(request):

    if request.user.role != "HOSPITAL":
        messages.error(
            request,
            "You are not authorized to access this page."
        )
        return redirect("home")

    hospital = request.user.hospital_profile

    if hospital.verification_status != "VERIFIED":
        return render(
            request,
            "hospitals/pending_verification.html",
            {"hospital": hospital}
        )

    return render(
        request,
        "hospitals/dashboard.html",
        {"hospital": hospital}
    )
