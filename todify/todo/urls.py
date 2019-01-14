from django.urls import path

from .views import (
    task_create,
    task_update,
    task_delete,
    task_completed,
    task_completed_list,
    ordered_tasks_ajax,
)


app_name = 'todo'
urlpatterns = [
    path('create/', task_create, name='task-create'),
    path('<int:pk>/update/', task_update, name='task-update'),
    path('<int:pk>/delete/', task_delete, name='task-delete'),
    path('<int:pk>/completed/', task_completed, name='task-completed'),
    path('completed/', task_completed_list, name='task-completed-list'),
    path('ajax/order_tasks/', ordered_tasks_ajax, name='ajax-ordered-task'),
]
