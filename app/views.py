from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from datetime import datetime
from app.models import FixedCost, Income
from app.serializers import FixedCostSerializer, IncomeSerializer
from collections import defaultdict
from dateutil.relativedelta import relativedelta

class FixedCostListView(APIView):

    def get(self, request):
        fixed_costs = FixedCost.objects.all()
        serialized_data = FixedCostSerializer(fixed_costs, many=True).data

        grouped_data = defaultdict(list)

        for item in serialized_data:
            date_from = datetime.strptime(item['date_from'], "%Y-%m")
            date_to = datetime.strptime(item['date_to'], "%Y-%m")

            # Generar los meses entre la fecha de inicio y la fecha de fin
            current_date = date_from
            while current_date <= date_to:
                month_key = current_date.strftime("%Y-%m")
                grouped_data[month_key].append({
                    "name": item['name'],
                    "price": item['price'],
                    "date_from": item['date_from'],
                    "date_to": item['date_to']
                })
                current_date += relativedelta(months=1)

        response_data = [
            {
                "date": month,
                "fixedCost": costs
            }
            for month, costs in grouped_data.items()
        ]

        return Response(response_data)

    def post(self, request):
            serializer = FixedCostSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        new_data = request.data

        existing_record = FixedCost.objects.filter(
            name=new_data['name'],
            date_from=new_data['date_from'],
        ).first()

        # Si encontramos un registro con los mismos name y date_from actualizar ese registro
        if existing_record:
            serializer = FixedCostSerializer(existing_record, data=new_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Modificar los registros anteriores para evitar la superposición de fechas
        existing_fixed_costs = FixedCost.objects.filter(name=new_data['name'])
        for fixed_cost in existing_fixed_costs:
            if fixed_cost.date_to >= new_data['date_from']:
                fixed_cost.date_to = (datetime.strptime(new_data['date_from'], "%Y-%m") - relativedelta(months=1)).strftime("%Y-%m")
                fixed_cost.save()

        return self.post(request)

    def delete(self, request):
            name_to_delete = request.data.get('name')

            if not name_to_delete:
                return Response({"detail": "Name is required."}, status=status.HTTP_400_BAD_REQUEST)

            fixed_costs = FixedCost.objects.filter(name=name_to_delete)

            if not fixed_costs.exists():
                return Response({"detail": f"'{name_to_delete}' not found."}, status=status.HTTP_404_NOT_FOUND)

            fixed_costs.delete()

            return Response({"detail": f"'{name_to_delete}' deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
class IncomeListView(APIView):

    def get(self, request):
        fixed_costs = Income.objects.all()
        serialized_data = IncomeSerializer(fixed_costs, many=True).data

        grouped_data = defaultdict(list)

        for item in serialized_data:
            date_from = datetime.strptime(item['date_from'], "%Y-%m")
            date_to = datetime.strptime(item['date_to'], "%Y-%m")

            # Generar los meses entre la fecha de inicio y la fecha de fin
            current_date = date_from
            while current_date <= date_to:
                month_key = current_date.strftime("%Y-%m")
                grouped_data[month_key].append({
                    "name": item['name'],
                    "price": item['price'],
                    "date_from": item['date_from'],
                    "date_to": item['date_to']
                })
                current_date += relativedelta(months=1)

        response_data = [
            {
                "date": month,
                "fixedCost": costs
            }
            for month, costs in grouped_data.items()
        ]

        return Response(response_data)

    def post(self, request):
            serializer = IncomeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        new_data = request.data

        existing_record = Income.objects.filter(
            name=new_data['name'],
            date_from=new_data['date_from'],
        ).first()

        # Si encontramos un registro con los mismos name y date_from actualizar ese registro
        if existing_record:
            serializer = IncomeSerializer(existing_record, data=new_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Modificar los registros anteriores para evitar la superposición de fechas
        existing_fixed_costs = Income.objects.filter(name=new_data['name'])
        for fixed_cost in existing_fixed_costs:
            if fixed_cost.date_to >= new_data['date_from']:
                fixed_cost.date_to = (datetime.strptime(new_data['date_from'], "%Y-%m") - relativedelta(months=1)).strftime("%Y-%m")
                fixed_cost.save()

        return self.post(request)

    def delete(self, request):
            name_to_delete = request.data.get('name')

            if not name_to_delete:
                return Response({"detail": "Name is required."}, status=status.HTTP_400_BAD_REQUEST)

            fixed_costs = Income.objects.filter(name=name_to_delete)

            if not fixed_costs.exists():
                return Response({"detail": f"'{name_to_delete}' not found."}, status=status.HTTP_404_NOT_FOUND)

            fixed_costs.delete()

            return Response({"detail": f"'{name_to_delete}' deleted successfully."}, status=status.HTTP_204_NO_CONTENT)