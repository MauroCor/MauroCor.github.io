from django.urls import path
from .views import CardSpendListView, FixedCostListView, IncomeListView

urlpatterns = [
    path('api/fixed-cost/', FixedCostListView.as_view(), name='fixed_cost'),
    path('api/income/', IncomeListView.as_view(), name='income'),
    path('api/card-spend/', CardSpendListView.as_view(), name='card_spend'),
    path('api/card-spend/<int:pk>/', CardSpendListView.as_view(), name='cardspend-delete'),
]
