from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create/', views.create_task, name='create_task'),
    path('all-tasks/', views.all_tasks, name='all_tasks'),
    path('update/<int:pk>/', views.update_task, name='update_task'),
    path('delete/<int:pk>/', views.delete_task, name='delete_task'),
    path('toggle-completion/<int:pk>/', views.toggle_completion, name='toggle_completion'),
]
