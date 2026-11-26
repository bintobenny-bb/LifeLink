from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/ai/", include("ai_assistant.urls")),
    path("accounts/", include("accounts.urls")),
    path('', views.home, name='home'),
    path("donors/", include("donors.urls")),
    path("patients/", include("patients.urls")),
    path("hospitals/", include("hospitals.urls")),
    path("lifelink-admin/", views.admin_dashboard, name="admin_dashboard"),
    path("lifelink-admin/hospitals/",
         views.hospital_management, name="hospital_management"),
    path("lifelink-admin/hospitals/<int:hospital_id>/verify/<str:status>/", views.update_hospital_verification, name="update_hospital_verification"
         ),
]
