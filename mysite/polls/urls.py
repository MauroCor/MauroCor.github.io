from django.urls import path

from . import views

urlpatterns = [
    path("monthly", views.gets_monthly, name="gets_monthly"),
    path('set_fixed_cost', views.set_fixed_cost, name='set_fixed_cost'),
    path('set_earning', views.set_earning, name='set_earning'),
    path('delete_fixed_cost/<int:fixed_cost_id>', views.delete_fixed_cost, name='delete_fixed_cost'),
    path('delete_earning/<int:earning_id>', views.delete_earning, name='delete_earning'),
    path('card', views.gets_card, name='gets_card'),
    path('set_card_spend', views.set_card_spend, name='set_card_spend'),
    path('delete_card_spend/<int:card_spend_id>', views.delete_card_spend, name='delete_card_spend'),
]
