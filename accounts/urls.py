from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .views import (
    update_measurements,
    custom_logout,
    delete_account,
    SignupView,
    CustomLoginView,
    ProfileUpdateView,
    update_avatar,
)

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

    # Password reset
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='accounts/password_reset.html'
        ),
        name='password_reset'
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='accounts/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='accounts/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),

    path('update-avatar/', update_avatar, name='update_avatar'),
]
