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
]
