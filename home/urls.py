from django.urls import path
from . import views
from .views import index

urlpatterns = [
    path('', index, name='home'),
    path('plan/', views.plan_view, name='plan'),
    path('contact/', views.contact, name='contact'),
    path(
        'clear-success-flag/',
        views.clear_success_flag,
        name='clear_success_flag'
        )
]
