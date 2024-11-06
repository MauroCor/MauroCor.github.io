from rest_framework import serializers
from datetime import datetime

from app.models import FixedCost

class FixedCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = FixedCost
        fields = ('name', 'price', 'date_from', 'date_to')
        extra_kwargs = {
            'date_to': {'required': False}  # Asegura que 'date_to' no sea obligatorio
        }

    def validate(self, data):
        # Convertir la fecha 'date_from' de string a datetime
        date_from = datetime.strptime(data.get('date_from'), "%Y-%m")

        # Si no se proporciona 'date_to', lo configuramos como un año después de 'date_from'
        if not data.get('date_to'):
            date_to = date_from.replace(year=date_from.year + 1)
            data['date_to'] = date_to.strftime("%Y-%m")  # Convierte de nuevo a formato string
        
        # Validar si 'date_to' no es menor a 'date_from'
        elif data.get('date_to'):
            date_to = datetime.strptime(data['date_to'], "%Y-%m")
            if date_to < date_from:
                raise serializers.ValidationError("La fecha de fin no puede ser anterior a la fecha de inicio.")
        
        return data
