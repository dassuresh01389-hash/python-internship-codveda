from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "created_by", "priority", "completed", "due_date", "created_at")
    list_filter = ("completed", "priority", "created_at")
    search_fields = ("title", "description", "created_by__username")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
