from django.urls import path
from .views import CardSpendListView, FixedCostListView, IncomeListView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/fixed-cost/', FixedCostListView.as_view(), name='fixed_cost'),
    path('api/income/', IncomeListView.as_view(), name='income'),
    path('api/card-spend/', CardSpendListView.as_view(), name='card_spend'),
    path('api/card-spend/<int:pk>/', CardSpendListView.as_view(), name='cardspend-delete'),
]
