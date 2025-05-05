from django.urls import path
from . import views
from .views import (
    update_measurements,
    custom_logout,
    delete_account,
    SignupView,
    CustomLoginView,
    ProfileUpdateView,
)
from .views import update_avatar


urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path(
        'login-update-measurements/',
        views.login_update_measurements,
        name='login_update_measurements'
    ),
    path(
        'update-measurements/',
        update_measurements,
        name='update_measurements'
    ),
    path(
        'delete-measurements/',
        views.delete_measurements,
        name='delete_measurements'
    ),
    path('logout/', custom_logout, name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path(
        'update-profile/',
        ProfileUpdateView.as_view(),
        name='update_profile'
        ),
    path('delete-account/', delete_account, name='delete_account'),
    path('update-avatar/', update_avatar, name='update_avatar'),
]
