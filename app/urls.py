from rest_framework import routers
from app.api import FixedCostViewSet

router = routers.DefaultRouter()

router.register('api/fixed-cost', FixedCostViewSet, 'fixed-cost')

urlpatterns = router.urls

# from . import views
# urlpatterns = [
#     path('monthly', views.gets_monthly, name='monthly'),
#     path('set-fixed-cost', views.set_fixed_cost, name='set_fixed_cost'),
#     path('set-earning', views.set_earning, name='set_earning'),
#     path('set-note', views.set_note, name='set_note'),
#     path('delete-fixed-cost/<str:fixed_cost_name>', views.delete_fixed_cost, name='delete_fixed_cost'),
#     path('delete-earning/<str:earning_name>', views.delete_earning, name='delete_earning'),
#     path('card', views.gets_card, name='card'),
#     path('set-card-spend', views.set_card_spend, name='set_card_spend'),
#     path('delete-card-spend/<int:card_spend_id>', views.delete_card_spend, name='delete_card_spend'),
#     path('edit-card-spend/<str:old_name>/<str:new_name>/', views.edit_card_spend, name='edit_card_spend'),
#     path('edit-fixed-cost/<str:old_name>/<str:new_name>/', views.edit_fixed_cost, name='edit_fixed_cost'),
#     path('edit-earning/<str:old_name>/<str:new_name>/', views.edit_earning, name='edit_earning'),
# ]
