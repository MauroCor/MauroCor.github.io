from django.urls import path

from . import views

urlpatterns = [
    path('monthly', views.gets_monthly, name='monthly'),
    path('set-fixed-cost', views.set_fixed_cost, name='set_fixed_cost'),
    path('set-earning', views.set_earning, name='set_earning'),
    path('delete-fixed_cost/<str:fixed_cost_name>', views.delete_fixed_cost, name='delete_fixed_cost'),
    path('delete-earning/<str:earning_name>', views.delete_earning, name='delete_earning'),
    path('card', views.gets_card, name='card'),
    path('set-card-spend', views.set_card_spend, name='set_card_spend'),
    path('delete-card-spend/<int:card_spend_id>', views.delete_card_spend, name='delete_card_spend'),
]
