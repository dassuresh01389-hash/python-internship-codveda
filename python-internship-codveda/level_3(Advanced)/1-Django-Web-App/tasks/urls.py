from django.urls import path

from . import views

urlpatterns = [
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("tasks/", views.task_list_view, name="task_list"),
    path("tasks/add/", views.task_create_view, name="task_create"),
    path("tasks/<int:pk>/edit/", views.task_edit_view, name="task_edit"),
    path("tasks/<int:pk>/delete/", views.task_delete_view, name="task_delete"),
    path("tasks/<int:pk>/toggle/", views.task_toggle_complete_view, name="task_toggle_complete"),
]
