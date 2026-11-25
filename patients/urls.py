from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_patient, name="register_patient"),
    path("dashboard/", views.patient_dashboard, name="patient_dashboard"),
]
