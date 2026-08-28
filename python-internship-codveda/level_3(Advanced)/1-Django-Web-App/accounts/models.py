from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """
    Extends Django's built-in User model with an application-specific role.

    We deliberately do NOT store passwords here or anywhere else -
    Django's auth system already hashes and stores passwords securely
    on the User model.
    """

    ROLE_ADMIN = "admin"
    ROLE_USER = "user"
    ROLE_CHOICES = [
        (ROLE_ADMIN, "Admin"),
        (ROLE_USER, "Regular User"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_USER)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["user__username"]

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

    @property
    def is_admin_role(self):
        return self.role == self.ROLE_ADMIN


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Automatically create a Profile whenever a new User is created.

    Django superusers (created via createsuperuser) are automatically
    given the 'admin' role so they see the same admin-oriented UI.
    """
    if created:
        role = Profile.ROLE_ADMIN if instance.is_superuser else Profile.ROLE_USER
        Profile.objects.create(user=instance, role=role)
    else:
        # Keep profile role in sync if a user is promoted to superuser later.
        profile, _ = Profile.objects.get_or_create(user=instance)
        if instance.is_superuser and profile.role != Profile.ROLE_ADMIN:
            profile.role = Profile.ROLE_ADMIN
            profile.save()
