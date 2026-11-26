from accounts.models import User
from hospitals.models import HospitalProfile
from donors.models import DonorProfile
from inventory.models import BloodInventory
from django.utils import timezone
from django.db.models import Sum
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from hospitals.models import HospitalProfile


def home(request):
    return render(request, 'home.html')


@login_required
def admin_dashboard(request):
    if request.user.role != "ADMIN" or not request.user.is_staff:
        messages.error(
            request,
            "You are not authorized to access the admin dashboard."
        )
        return redirect("home")

    total_users = User.objects.count()

    total_hospitals = HospitalProfile.objects.count()

    total_donors = DonorProfile.objects.count()

    available_units = BloodInventory.objects.filter(
        hospital__verification_status=HospitalProfile.VerificationStatus.VERIFIED,
        inventory_status=BloodInventory.InventoryStatus.AVAILABLE,
        testing_status=BloodInventory.TestingStatus.CLEARED,
        expiry_date__gt=timezone.localdate(),
        units_available__gt=0
    ).aggregate(
        total=Sum("units_available")
    )["total"] or 0

    context = {
        "total_users": total_users,
        "total_hospitals": total_hospitals,
        "total_donors": total_donors,
        "available_units": available_units,
    }

    return render(
        request,
        "admin_dashboard/index.html",
        context
    )


@login_required
def hospital_management(request):
    if request.user.role != "ADMIN" or not request.user.is_staff:
        messages.error(
            request,
            "You are not authorized to access hospital management."
        )
        return redirect("home")

    search_query = request.GET.get("q", "").strip()

    hospitals = HospitalProfile.objects.all().order_by("-created_at")

    if search_query:
        hospitals = hospitals.filter(
            hospital_name__icontains=search_query
        ) | hospitals.filter(
            registration_number__icontains=search_query
        )

    context = {
        "hospitals": hospitals,
        "search_query": search_query,
        "total_hospitals": HospitalProfile.objects.count(),
        "pending_hospitals": HospitalProfile.objects.filter(
            verification_status="PENDING"
        ).count(),
        "verified_hospitals": HospitalProfile.objects.filter(
            verification_status="VERIFIED"
        ).count(),
        "rejected_hospitals": HospitalProfile.objects.filter(
            verification_status="REJECTED"
        ).count(),
    }

    return render(
        request,
        "admin_dashboard/hospitals.html",
        context
    )


@login_required
@require_POST
def update_hospital_verification(request, hospital_id, status):
    if request.user.role != "ADMIN" or not request.user.is_staff:
        messages.error(
            request,
            "You are not authorized to perform this action."
        )
        return redirect("home")

    hospital = get_object_or_404(
        HospitalProfile,
        id=hospital_id
    )

    if status not in [
        HospitalProfile.VerificationStatus.VERIFIED,
        HospitalProfile.VerificationStatus.REJECTED,
    ]:
        messages.error(request, "Invalid verification action.")
        return redirect("hospital_management")

    hospital.verification_status = status
    hospital.save()

    if status == HospitalProfile.VerificationStatus.VERIFIED:
        messages.success(
            request,
            f"{hospital.hospital_name} has been successfully verified."
        )
    else:
        messages.warning(
            request,
            f"{hospital.hospital_name} has been rejected."
        )

    return redirect("hospital_management")
