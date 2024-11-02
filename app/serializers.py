from rest_framework import serializers
from .models import FixedCost

class FixedCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = FixedCost
        fields = ('id', 'month', 'name', 'price')
