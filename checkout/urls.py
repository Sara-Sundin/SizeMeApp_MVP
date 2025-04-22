from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path('wh/', webhook, name='webhook'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/success/<str:order_number>/', views.checkout_success, name='checkout_success'),
]