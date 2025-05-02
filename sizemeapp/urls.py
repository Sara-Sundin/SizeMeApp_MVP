from django.urls import path
from . import views

urlpatterns = [
    path('toggle-size-mode/', views.toggle_size_mode, name='toggle_size_mode'),
    path('size-recommendation/<int:product_id>/', views.size_recommendation_view, name='size_recommendation'),
]
