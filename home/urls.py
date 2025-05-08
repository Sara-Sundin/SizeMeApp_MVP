from django.urls import path
from . import views
from .views import index
from .views import custom_logout

urlpatterns = [
    path('', index, name='home'),
    path('plan/', views.plan_view, name='plan'),
    path('contact/', views.contact, name='contact'),
    path('logout/', custom_logout, name='custom_logout'),
    path(
        'clear-success-flag/',
        views.clear_success_flag,
        name='clear_success_flag'
        )
]
