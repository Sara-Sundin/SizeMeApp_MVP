# accounts/urls.py
from django.urls import path
from . import views
from .views import SignupView, CustomLoginView, ProfileUpdateView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('update-profile/', ProfileUpdateView.as_view(), name='update_profile'),
]

