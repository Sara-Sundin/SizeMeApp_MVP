from django.urls import path
from . import views

urlpatterns = [
    path('toggle-size-mode/', views.toggle_size_mode, name='toggle_size_mode'),
]
