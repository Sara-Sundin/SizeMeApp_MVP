from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path('wh/', webhook, name='webhook'),
    path('checkout/', views.checkout, name='checkout'),
    path(
        'checkout/success/<str:order_number>/',
        views.checkout_success, name='checkout_success'),
    path('order-history/', views.order_history, name='order_history'),
    path('order/<str:order_number>/', views.order_detail, name='order_detail'),
]
