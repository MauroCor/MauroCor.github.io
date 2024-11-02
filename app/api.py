from .models import FixedCost
from rest_framework import viewsets, permissions
from .serializers import FixedCostSerializer

class FixedCostViewSet(viewsets.ModelViewSet):
    queryset = FixedCost.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = FixedCostSerializer