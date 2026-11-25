
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from accounts.models import User
from .forms import DonorProfileForm


@login_required
def register_donor(request):

    if request.user.role != User.Role.INDIVIDUAL:
        messages.error(
            request, "You are not authorized to register as a donor.")
        return redirect("home")

    if hasattr(request.user, "donor_profile"):
        return redirect("donor_dashboard")

    if request.method == "POST":
        form = DonorProfileForm(request.POST)

        if form.is_valid():
            donor_profile = form.save(commit=False)
            donor_profile.user = request.user
            donor_profile.save()

            messages.success(
                request,
                "Your donor profile has been created successfully!"
            )
            return redirect("donor_dashboard")

    else:
        form = DonorProfileForm()

    return render(
        request,
        "donors/register.html",
        {"form": form}
    )


@login_required
def donor_dashboard(request):

    if request.user.role != User.Role.INDIVIDUAL:
        messages.error(request, "You are not authorized to access this page.")
        return redirect("home")

    if not hasattr(request.user, "donor_profile"):
        return redirect("register_donor")

    return render(
        request,
        "donors/dashboard.html",
        {"donor": request.user.donor_profile}
    )
