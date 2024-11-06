from collections import defaultdict
from datetime import datetime
from dateutil.relativedelta import relativedelta
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import FixedCost
from .serializers import FixedCostSerializer
from rest_framework import status

class FixedCostListView(APIView):
    
    def get(self, request):
        # Obtenemos todos los gastos fijos
        fixed_costs = FixedCost.objects.all()
        serialized_data = FixedCostSerializer(fixed_costs, many=True).data

        # Agrupar los costos fijos por mes
        grouped_data = defaultdict(list)
        
        for item in serialized_data:
            # Convertimos las fechas a tipo datetime
            date_from = datetime.strptime(item['date_from'], "%Y-%m")
            date_to = datetime.strptime(item['date_to'], "%Y-%m")

            # Genera cada mes en el intervalo entre date_from y date_to
            current_date = date_from
            while current_date <= date_to:
                month_key = current_date.strftime("%Y-%m")
                grouped_data[month_key].append({
                    "name": item['name'],
                    "price": item['price'],
                    "date_from": item['date_from'],
                    "date_to": item['date_to']
                })
                # Aumentamos un mes a la fecha actual
                current_date += relativedelta(months=1)

        # Formato de respuesta agrupado por fecha
        response_data = [
            {
                "date": month,
                "fixedCost": costs
            }
            for month, costs in grouped_data.items()
        ]

        return Response(response_data)

    def post(self, request):
        # Creamos el serializer con los datos del request
        serializer = FixedCostSerializer(data=request.data)
        
        # Validamos si los datos del serializer son correctos
        if serializer.is_valid():
            # Aquí no es necesario hacer la lógica de 'date_to', ya que el serializer se encarga
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Si los datos no son válidos, respondemos con un error
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
