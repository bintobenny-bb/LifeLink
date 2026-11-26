
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),

    path(
        "login/",
        views.RoleBasedLoginView.as_view(),
        name="login"
    ),

    path("dashboard/", views.dashboard, name="dashboard"),

    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout"
    ),
]
