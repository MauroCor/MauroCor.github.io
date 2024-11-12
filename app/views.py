from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from datetime import datetime
from app.models import CardSpend, FixedCost, Income
from app.serializers import CardSpendSerializer, FixedCostSerializer, IncomeSerializer
from collections import defaultdict
from dateutil.relativedelta import relativedelta

class FixedCostListView(APIView):

    def get(self, request):
        fixed_costs = FixedCost.objects.all()
        serialized_data = FixedCostSerializer(fixed_costs, many=True).data

        grouped_data = defaultdict(lambda: {"fixedCost": [], "total": 0})

        for item in serialized_data:
            date_from = datetime.strptime(item['date_from'], "%Y-%m")
            date_to = datetime.strptime(item['date_to'], "%Y-%m")

            current_date = date_from
            while current_date < date_to:
                month_key = current_date.strftime("%Y-%m")
                price = int(item['price'])
                
                grouped_data[month_key]["fixedCost"].append({
                    "name": item['name'],
                    "price": price,
                    "date_from": item['date_from'],
                    "date_to": item['date_to']
                })
                grouped_data[month_key]["total"] += price
                current_date += relativedelta(months=1)

        # Obtener CardSpend
        card_spends = CardSpend.objects.all()

        for card_spend in card_spends:
            date_from = datetime.strptime(card_spend.date_from, "%Y-%m")
            price = card_spend.price
            fees = card_spend.fees

            monthly_payment = price / fees

            for fee_num in range(1, fees + 1):
                month_key = date_from.strftime("%Y-%m")
                grouped_data[month_key]["total"] += monthly_payment
                date_from += relativedelta(months=1)

        for month_key, data in grouped_data.items():
            tarjeta_total = 0
            for card_spend in card_spends:
                date_from = datetime.strptime(card_spend.date_from, "%Y-%m")
                price = card_spend.price
                fees = card_spend.fees
                date_to = date_from + relativedelta(months=fees-1)

                if date_from <= datetime.strptime(month_key, "%Y-%m") <= date_to:
                    monthly_payment = price / fees
                    tarjeta_total += monthly_payment

            if tarjeta_total > 0:
                data["fixedCost"].append({
                    "name": "Tarjeta",
                    "price": round(tarjeta_total)
                })

        # Respuesta por fecha y orden cronologico
        response_data = sorted([
            {
                "date": month,
                "fixedCost": data["fixedCost"],
                "total": round(data["total"])
            }
            for month, data in grouped_data.items()
        ], key=lambda x: x["date"])

        return Response(response_data)

    def post(self, request):
            serializer = FixedCostSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        new_data = request.data
        new_date_to = new_data.get('date_to')

        if not new_date_to:
            return Response({"detail": "'date_to' is required."}, status=status.HTTP_400_BAD_REQUEST)

        existing_record = FixedCost.objects.filter(
            name=new_data['name'],
            date_from=new_data['date_from'],
        ).first()
        
        if existing_record:
            if new_date_to == new_data['date_from']:
                existing_record.delete()
                return Response({"detail": "Element deleted."}, status=status.HTTP_204_NO_CONTENT)
  
            serializer = FixedCostSerializer(existing_record, data={'date_to': new_date_to}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "element not found."}, status=status.HTTP_404_NOT_FOUND)
    
class IncomeListView(APIView):

    def get(self, request):
        income = Income.objects.all()
        serialized_data = IncomeSerializer(income, many=True).data

        grouped_data = defaultdict(lambda: {"income": [], "total": 0})

        for item in serialized_data:
            date_from = datetime.strptime(item['date_from'], "%Y-%m")
            date_to = datetime.strptime(item['date_to'], "%Y-%m")

            # Generar los meses entre la fecha de inicio y la fecha de fin
            current_date = date_from
            while current_date < date_to:
                month_key = current_date.strftime("%Y-%m")
                price = int(item['price'])
                
                # Agregar el registro al mes correspondiente y sumar su precio al total del mes
                grouped_data[month_key]["income"].append({
                    "name": item['name'],
                    "price": price,
                    "date_from": item['date_from'],
                    "date_to": item['date_to']
                })
                grouped_data[month_key]["total"] += price
                current_date += relativedelta(months=1)

        # Formato de respuesta agrupado por fecha y ordenado cronológicamente
        response_data = sorted([
            {
                "date": month,
                "income": data["income"],
                "total": data["total"]
            }
            for month, data in grouped_data.items()
        ], key=lambda x: x["date"])

        return Response(response_data)

    def post(self, request):
            serializer = IncomeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        new_data = request.data
        new_date_to = new_data.get('date_to')

        if not new_date_to:
            return Response({"detail": "'date_to' is required."}, status=status.HTTP_400_BAD_REQUEST)

        existing_record = Income.objects.filter(
            name=new_data['name'],
            date_from=new_data['date_from'],
        ).first()
        
        if existing_record:
            if new_date_to == new_data['date_from']:
                existing_record.delete()
                return Response({"detail": "Element deleted."}, status=status.HTTP_204_NO_CONTENT)
  
            serializer = IncomeSerializer(existing_record, data={'date_to': new_date_to}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "element not found."}, status=status.HTTP_404_NOT_FOUND)
    
class CardSpendListView(APIView):

    def get(self, request):
        card_spend = CardSpend.objects.all()
        serialized_data = CardSpendSerializer(card_spend, many=True).data

        grouped_data = defaultdict(lambda: {"cardSpend": [], "total": 0})

        for item in serialized_data:
            date_from = datetime.strptime(item['date_from'], "%Y-%m")
            price = int(item['price'])
            fees = int(item['fees'])

            # Generar cuotas para cada mes dentro del rango
            for fee_num in range(1, fees + 1):
                month_key = date_from.strftime("%Y-%m")
                
                grouped_data[month_key]["cardSpend"].append({
                    "id": item['id'],
                    "name": item['name'],
                    "price": price / fees,
                    "installment": f"{fee_num}/{fees}"
                })
                grouped_data[month_key]["total"] += price / fees
                date_from += relativedelta(months=1)

        # Formato de respuesta agrupado por fecha y ordenado cronológicamente
        response_data = sorted([
            {
                "date": month,
                "cardSpend": data["cardSpend"],
                "total": round(data["total"])
            }
            for month, data in grouped_data.items()
        ], key=lambda x: x["date"])

        return Response(response_data)

    def post(self, request):
            serializer = CardSpendSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            card_spend = CardSpend.objects.get(pk=pk)
            card_spend.delete()
            return Response({'message': 'Card spend deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except CardSpend.DoesNotExist:
            return Response({'error': 'Card spend not found'}, status=status.HTTP_404_NOT_FOUND)