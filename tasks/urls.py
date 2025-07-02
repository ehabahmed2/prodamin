from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create/', views.create_task, name='create_task'),
    path('all-tasks/', views.all_tasks, name='all_tasks'),
]
