"""
Root URL configuration for the Task Manager project.
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),

    # Accounts app: registration, login, logout, password reset, profile
    path("accounts/", include("accounts.urls")),

    # Redirect the bare root to the dashboard (dashboard view itself
    # redirects anonymous users to login via @login_required).
    path("", RedirectView.as_view(pattern_name="dashboard", permanent=False), name="home"),

    # Tasks app: dashboard + task CRUD
    path("", include("tasks.urls")),
]
