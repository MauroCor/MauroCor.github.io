from django.urls import path
from .views import FixedCostListView

urlpatterns = [
    path('api/fixed-cost/', FixedCostListView.as_view(), name='fixed-cost'),
]
