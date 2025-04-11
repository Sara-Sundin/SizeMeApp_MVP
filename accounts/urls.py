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
    path('update-measurements/', update_measurements, name='update_measurements'),
    path('logout/', custom_logout, name='logout'),
    path('update-profile/', ProfileUpdateView.as_view(), name='update_profile'),
    path('delete-account/', delete_account, name='delete_account'), 
]

