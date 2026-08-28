from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ProfileUpdateForm, RegisterForm


def register_view(request):
    """
    Handles new user registration.

    On success, the user is automatically logged in and redirected to
    their dashboard with a welcome message. Validation errors (duplicate
    username/email, password mismatch, weak password, etc.) are shown
    inline on the form via Django messages/form errors.
    """
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to Task Manager, {user.username}! Your account was created successfully.")
            return redirect("dashboard")
        else:
            messages.error(request, "Please correct the errors below and try again.")
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})


@login_required
def profile_view(request):
    """Displays and allows editing of the logged-in user's profile."""
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect("profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, "accounts/profile.html", {"form": form})
