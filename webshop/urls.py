from django.urls import path
from .views import webshop_view

urlpatterns = [
    path('', webshop_view, name='webshop'),
]
