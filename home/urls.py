from django.urls import path
from . import views
from .views import home_view

urlpatterns = [
    path('', home_view, name='home'),
    path('starter_plan/', views.starter_plan, name='starter_plan'),
]
