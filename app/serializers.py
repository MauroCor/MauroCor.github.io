from rest_framework import serializers
from datetime import datetime

from app.models import FixedCost, Income

class FixedCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = FixedCost
        fields = ('name', 'price', 'date_from', 'date_to')
        extra_kwargs = {
            'date_to': {'required': False, 'allow_null': True}
        }

    def validate(self, data):
            # Convertimos date_from y date_to a objetos datetime para la comparación
            date_from = datetime.strptime(data.get('date_from'), "%Y-%m")
            date_to = data.get('date_to')
            if date_to:
                date_to = datetime.strptime(date_to, "%Y-%m")
            else:
                # Si date_to no está especificado, asumir un año después de date_from
                date_to = date_from.replace(year=date_from.year + 1)
                data['date_to'] = date_to.strftime("%Y-%m")

            # Verificar si estamos en modo de actualización
            instance_id = self.instance.id if self.instance else None

            # Validar si ya existe un registro con el mismo nombre y fechas superpuestas (excluyendo el mismo registro en actualizaciones)
            overlapping_costs = FixedCost.objects.filter(
                name=data['name'],
                date_from__lte=date_to,
                date_to__gte=date_from
            ).exclude(id=instance_id)

            if overlapping_costs.exists():
                raise serializers.ValidationError(
                   f"'{data['name']}' already exist between these dates."
                )

            return data

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ('name', 'price', 'date_from', 'date_to')
        extra_kwargs = {
            'date_to': {'required': False, 'allow_null': True}
        }

    def validate(self, data):
            date_from = datetime.strptime(data.get('date_from'), "%Y-%m")
            date_to = data.get('date_to')
            if date_to:
                date_to = datetime.strptime(date_to, "%Y-%m")
            else:
                date_to = date_from.replace(year=date_from.year + 1)
                data['date_to'] = date_to.strftime("%Y-%m")

            instance_id = self.instance.id if self.instance else None

            overlapping_costs = Income.objects.filter(
                name=data['name'],
                date_from__lte=date_to,
                date_to__gte=date_from
            ).exclude(id=instance_id)

            if overlapping_costs.exists():
                raise serializers.ValidationError(
                   f"'{data['name']}' already exist between these dates."
                )

            return data
