from . import views
from django.urls import path
from .views import (
    update_measurements,
    custom_logout,
    delete_account,
    SignupView,
    CustomLoginView,
    ProfileUpdateView,
)


urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('login-update-measurements/', views.login_update_measurements, name='login_update_measurements'),
    path('update-measurements/', update_measurements, name='update_measurements'),
    path('delete-measurements/', views.delete_measurements, name='delete_measurements'),
    path('logout/', custom_logout, name='logout'),
    path('update-profile/', ProfileUpdateView.as_view(), name='update_profile'),
    path('delete-account/', delete_account, name='delete_account'), 
]

