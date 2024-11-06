from django.urls import path
from .views import FixedCostListView, IncomeListView

urlpatterns = [
    path('api/fixed-cost/', FixedCostListView.as_view(), name='fixed_cost'),
    path('api/income/', IncomeListView.as_view(), name='income'),
]
