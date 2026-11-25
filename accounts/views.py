from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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


@login_required
def dashboard(request):

    if request.user.role != User.Role.INDIVIDUAL:
        messages.error(
            request, "You are not authorized to access this dashboard.")
        return redirect("home")

    return render(
        request,
        "accounts/dashboard.html"
    )
