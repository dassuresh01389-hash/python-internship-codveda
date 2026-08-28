from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TaskForm
from .models import Task


def _is_admin(user):
    """Returns True if the given user has the 'admin' application role."""
    return user.is_superuser or getattr(getattr(user, "profile", None), "role", None) == "admin"


def _get_visible_tasks(user):
    """
    Admins can see every task in the system; regular users only see their
    own tasks. This enforces the "regular users cannot touch other users'
    tasks" requirement at the query level, not just in templates.
    """
    if _is_admin(user):
        return Task.objects.all()
    return Task.objects.filter(created_by=user)


@login_required
def dashboard_view(request):
    """
    Professional dashboard showing task statistics for the logged-in user
    (or, for admins, statistics across the whole system).
    """
    tasks = _get_visible_tasks(request.user)
    context = {
        "total_tasks": tasks.count(),
        "pending_tasks": tasks.filter(completed=False).count(),
        "completed_tasks": tasks.filter(completed=True).count(),
        "high_priority_tasks": tasks.filter(priority=Task.PRIORITY_HIGH, completed=False).count(),
        "recent_tasks": tasks.order_by("-created_at")[:5],
        "is_admin": _is_admin(request.user),
    }
    return render(request, "tasks/dashboard.html", context)


@login_required
def task_list_view(request):
    """
    Lists tasks belonging to the current user (or all tasks, for admins).
    Supports simple filtering via ?filter=pending|completed|all.
    """
    tasks = _get_visible_tasks(request.user)

    status_filter = request.GET.get("filter", "all")
    if status_filter == "pending":
        tasks = tasks.filter(completed=False)
    elif status_filter == "completed":
        tasks = tasks.filter(completed=True)

    context = {
        "tasks": tasks,
        "status_filter": status_filter,
        "is_admin": _is_admin(request.user),
    }
    return render(request, "tasks/task_list.html", context)


@login_required
def task_create_view(request):
    """Allows any logged-in user to create a new task owned by them."""
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            messages.success(request, f'Task "{task.title}" was created successfully.')
            return redirect("task_list")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = TaskForm()

    return render(request, "tasks/task_form.html", {"form": form, "form_title": "Add Task"})


def _check_task_permission(request, task):
    """
    Raises PermissionDenied unless the requesting user owns the task or
    is an admin. Used to protect edit/delete/toggle views so that regular
    users can never modify another user's tasks.
    """
    if task.created_by_id != request.user.id and not _is_admin(request.user):
        raise PermissionDenied("You do not have permission to modify this task.")


@login_required
def task_edit_view(request, pk):
    task = get_object_or_404(Task, pk=pk)
    _check_task_permission(request, task)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, f'Task "{task.title}" was updated successfully.')
            return redirect("task_list")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = TaskForm(instance=task)

    return render(
        request, "tasks/task_form.html", {"form": form, "form_title": "Edit Task", "task": task}
    )


@login_required
def task_delete_view(request, pk):
    task = get_object_or_404(Task, pk=pk)
    _check_task_permission(request, task)

    if request.method == "POST":
        title = task.title
        task.delete()
        messages.success(request, f'Task "{title}" was deleted.')
        return redirect("task_list")

    return render(request, "tasks/task_confirm_delete.html", {"task": task})


@login_required
def task_toggle_complete_view(request, pk):
    """Quickly marks a task as completed / not completed."""
    task = get_object_or_404(Task, pk=pk)
    _check_task_permission(request, task)

    task.completed = not task.completed
    task.save(update_fields=["completed", "updated_at"])

    status = "completed" if task.completed else "marked as pending"
    messages.success(request, f'Task "{task.title}" was {status}.')
    return redirect("task_list")
