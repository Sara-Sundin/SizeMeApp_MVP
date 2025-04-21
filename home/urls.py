from django.urls import path
from . import views
from .views import home_view

urlpatterns = [
    path('', home_view, name='home'),
    path('plan/', views.plan_view, name='plan'),

]
