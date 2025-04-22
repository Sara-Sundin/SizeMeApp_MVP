from django.urls import path
from . import views
from .views import index

urlpatterns = [
    path('', index, name='home'),
    path('plan/', views.plan_view, name='plan'),
]
