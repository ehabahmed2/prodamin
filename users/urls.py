from django.urls import path

from home import views
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),  # Login page
    path('register/', views.register_view, name='register'),  # Register page
    path('logout/', views.logout_view, name='logout'),  # Logout page
    path('profile/', views.update_profile, name='profile'),  # Profile page
]

