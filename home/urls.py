from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('starter_plan/', views.starter_plan, name='starter_plan'),
]
