from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path('wh/', webhook, name='webhook'),
    path('checkout/<int:plan_id>/', views.checkout_plan, name='checkout_plan'),
    path('checkout/success/<str:order_number>/', views.checkout_success, name='checkout_success'),
]