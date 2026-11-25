from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_donor, name="register_donor"),
    path(
        "dashboard/", views.donor_dashboard, name="donor_dashboard"
    ),
]
