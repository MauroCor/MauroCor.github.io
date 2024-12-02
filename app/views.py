from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from datetime import datetime
from app.models import CardSpend, FixedCost, Income, Saving
from app.serializers import CardSpendSerializer, FixedCostSerializer, IncomeSerializer, SavingSerializer
from collections import defaultdict
from dateutil.relativedelta import relativedelta
from rest_framework.permissions import IsAuthenticated
import yfinance as yf


class FixedCostListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        fixed_costs = FixedCost.objects.filter(user=request.user)
        serialized_data = FixedCostSerializer(
            fixed_costs, many=True, context={'request': request}).data

        grouped_data = defaultdict(lambda: {"fixedCost": [], "total": 0})
        exchg_rate = request.query_params.get('exchg_rate', 0)

        for item in serialized_data:
            date_from = datetime.strptime(item['date_from'], "%Y-%m")
            date_to = datetime.strptime(item['date_to'], "%Y-%m")

            current_date = date_from
            while current_date <= date_to:
                month_key = current_date.strftime("%Y-%m")
                if item['ccy'] == 'ARS':
                    price = int(item['price'])
                    grouped_data[month_key]["fixedCost"].append({
                        "name": item['name'],
                        "ccy": item['ccy'],
                        "price": price,
                        "date_from": item['date_from'],
                        "date_to": item['date_to']
                    })
                    grouped_data[month_key]["total"] += price
                    current_date += relativedelta(months=1)
                else:
                    price = int(item['price']) * int(exchg_rate)
                    grouped_data[month_key]["fixedCost"].append({
                        "name": item['name'],
                        "ccy": item['ccy'],
                        "amount": int(item['price']),
                        "price": price,
                        "exRate": exchg_rate,
                        "date_from": item['date_from'],
                        "date_to": item['date_to']
                    })
                    grouped_data[month_key]["total"] += price
                    current_date += relativedelta(months=1)

        # Obtener CardSpend
        card_spends = CardSpend.objects.filter(user=request.user)

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
                    "ccy": "ARS",
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
        request.data['user'] = request.user.id

        serializer = FixedCostSerializer(
            data=request.data, context={'request': request})
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
            user=request.user
        ).first()

        if existing_record:
            if new_date_to < new_data['date_from']:
                existing_record.delete()
                return Response({"detail": "Element deleted."}, status=status.HTTP_204_NO_CONTENT)

            serializer = FixedCostSerializer(existing_record, data={
                                             'date_to': new_date_to}, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Element not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        new_data = request.data
        existing_record = FixedCost.objects.filter(
            name=new_data['name'],
            date_from=new_data['date_from'],
        ).first()

        # Si encontramos un registro con los mismos name y date_from actualizar ese registro
        if existing_record:
            serializer = FixedCostSerializer(
                existing_record, data=new_data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Modificar los registros anteriores para evitar la superposición de fechas
        existing_fixed_costs = FixedCost.objects.filter(name=new_data['name'])
        for fixed_cost in existing_fixed_costs:
            if fixed_cost.date_to >= new_data['date_from']:
                fixed_cost.date_to = (datetime.strptime(
                    new_data['date_from'], "%Y-%m") - relativedelta(months=1)).strftime("%Y-%m")
                fixed_cost.save()

        return self.post(request)


class IncomeListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        income = Income.objects.filter(user=request.user)
        serialized_data = IncomeSerializer(
            income, many=True, context={'request': request}).data

        grouped_data = defaultdict(lambda: {"income": [], "total": 0})
        exchg_rate = request.query_params.get('exchg_rate', 0)

        for item in serialized_data:
            date_from = datetime.strptime(item['date_from'], "%Y-%m")
            date_to = datetime.strptime(item['date_to'], "%Y-%m")

            # Generar los meses entre la fecha de inicio y la fecha de fin
            current_date = date_from
            while current_date <= date_to:
                month_key = current_date.strftime("%Y-%m")
                if item['ccy'] == 'ARS':
                    price = int(item['price'])
                    grouped_data[month_key]["income"].append({
                        "name": item['name'],
                        "ccy": item['ccy'],
                        "price": price,
                        "date_from": item['date_from'],
                        "date_to": item['date_to']
                    })
                    grouped_data[month_key]["total"] += price
                    current_date += relativedelta(months=1)
                else:
                    price = int(item['price']) * int(exchg_rate)
                    grouped_data[month_key]["income"].append({
                        "name": item['name'],
                        "ccy": item['ccy'],
                        "amount": int(item['price']),
                        "price": price,
                        "exRate": exchg_rate,
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
        request.data['user'] = request.user.id
        serializer = IncomeSerializer(
            data=request.data, context={'request': request})
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
            user=request.user
        ).first()

        if existing_record:
            if new_date_to < new_data['date_from']:
                existing_record.delete()
                return Response({"detail": "Element deleted."}, status=status.HTTP_204_NO_CONTENT)

            serializer = IncomeSerializer(existing_record, data={
                                          'date_to': new_date_to}, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "element not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        new_data = request.data

        existing_record = Income.objects.filter(
            name=new_data['name'],
            date_from=new_data['date_from'],
        ).first()

        # Si encontramos un registro con los mismos name y date_from actualizar ese registro
        if existing_record:
            serializer = IncomeSerializer(
                existing_record, data=new_data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Modificar los registros anteriores para evitar la superposición de fechas
        existing_incomes = Income.objects.filter(name=new_data['name'])
        for income in existing_incomes:
            if income.date_to >= new_data['date_from']:
                income.date_to = (datetime.strptime(
                    new_data['date_from'], "%Y-%m") - relativedelta(months=1)).strftime("%Y-%m")
                income.save()

        return self.post(request)


class CardSpendListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        card_spend = CardSpend.objects.filter(user=request.user)
        serialized_data = CardSpendSerializer(
            card_spend, many=True, context={'request': request}).data

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
        request.data['user'] = request.user.id
        serializer = CardSpendSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            card_spend = CardSpend.objects.get(pk=pk, user=request.user)
            card_spend.delete()
            return Response({'message': 'Card spend deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except CardSpend.DoesNotExist:
            return Response({'error': 'Card spend not found'}, status=status.HTTP_404_NOT_FOUND)


class SavingListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        saving = Saving.objects.filter(user=request.user)
        serialized_data = SavingSerializer(
            saving, many=True, context={'request': request}).data

        grouped_data = defaultdict(lambda: {"saving": [], "total": 0})
        exchg_rate = request.query_params.get('exchg_rate', 0)

        for item in serialized_data:
            date_from = datetime.strptime(item['date_from'], "%Y-%m")
            date_to = datetime.strptime(item['date_to'], "%Y-%m")
            current_date = date_from
            
            # var
            previous_obtained = None
            price = None
            previous_price = None
            searched_tickers = {}

            while current_date <= date_to:
                month_key = current_date.strftime("%Y-%m")
                invested = int(item['invested'])

                if item['type'] == 'fijo':
                    months = (datetime.strptime(item['date_to'], "%Y-%m").year - datetime.strptime(item['date_from'], "%Y-%m").year) * \
                        12 + datetime.strptime(item['date_to'], "%Y-%m").month - datetime.strptime(
                            item['date_from'], "%Y-%m").month
                    tna = round(
                        ((int(item['obtained']) / int(item['invested'])) - 1) / months * 12 * 100, 0)
                    liquid = current_date == date_to
                    obtained = int(item['obtained']) if liquid else 0

                elif item['type'] == 'flex':
                    liquid = True
                    tna = float(item['tna'])
                    if previous_obtained is not None:
                        obtained = previous_obtained + previous_obtained * (tna / 12 / 100)
                    else:
                        obtained = invested

                elif item['type'] == 'var':
                    liquid = current_date == date_to
                    ticker = item['name']
                    
                    if ticker in searched_tickers:
                        history_prices = searched_tickers[ticker]
                        price = history_prices.get(month_key, previous_price)
                        obtained = price * int(item['qty'])
                    else:
                        history_prices = PricesListView.get_historical_prices(self, ticker, month_key)
                        
                        if history_prices == 0:
                            searched_tickers[ticker] = {}
                            obtained = 0
                        else:
                            searched_tickers[ticker] = history_prices
                            price = history_prices.get(month_key, previous_price)
                            if price == None: price = invested
                            obtained = price * int(item['qty'])

                    tna = (obtained - invested) * 100 / invested


                # Agregar información al grupo
                grouped_data[month_key]["saving"].append({
                    "id": item['id'],
                    "name": item['name'],
                    "type": item['type'],
                    "invested": invested,
                    "ccy": item['ccy'],
                    "obtained": int(obtained),
                    "date_from": item['date_from'],
                    "date_to": item['date_to'],
                    "tna": round(tna,1),
                    "qty": item['qty'],
                    "liquid": liquid
                })

                # Calcular total del mes
                if liquid or item['type'] == 'var':
                    if item['ccy'] == 'ARS':
                        grouped_data[month_key]["total"] += int(obtained)
                    else:
                        grouped_data[month_key]["total"] += int(obtained) * int(exchg_rate)
                else:
                    if item['ccy'] == 'ARS':
                        grouped_data[month_key]["total"] += invested
                    else:
                        grouped_data[month_key]["total"] += invested * int(exchg_rate)


                # Actualizar valores
                previous_price = price
                previous_obtained = obtained
                current_date += relativedelta(months=1)

        response_data = sorted([
            {
                "date": month,
                "saving": data["saving"],
                "total": data["total"]
            }
            for month, data in grouped_data.items()
        ], key=lambda x: x["date"])

        return Response(response_data)

    def post(self, request):
        request.data['user'] = request.user.id
        serializer = SavingSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            card_spend = Saving.objects.get(pk=pk, user=request.user)
            card_spend.delete()
            return Response({'message': 'Saving deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except CardSpend.DoesNotExist:
            return Response({'error': 'Saving not found'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        new_data = request.data
        new_date_to = new_data.get('date_to')

        if not new_date_to:
            return Response({"detail": "'date_to' is required."}, status=status.HTTP_400_BAD_REQUEST)

        existing_record = Saving.objects.get(pk=pk, user=request.user)

        if existing_record:
            if new_date_to < new_data['date_from']:
                existing_record.delete()
                return Response({"detail": "Element deleted."}, status=status.HTTP_204_NO_CONTENT)

            serializer = SavingSerializer(existing_record, data={
                                          'date_to': new_date_to}, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "element not found."}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request):
        new_data = request.data
        if new_data['type'] == 'flex' or new_data['type'] == 'var':
            existing_record = Saving.objects.filter(
                name=new_data['name'],
                type=new_data['type'],
                date_from=new_data['date_from'],
            ).first()

            if existing_record:
                serializer = SavingSerializer(
                    existing_record, data=new_data, partial=True, context={'request': request})
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Modificar los registros anteriores para evitar la superposición de fechas
            existing_savings = Saving.objects.filter(name=new_data['name'])
            for saving in existing_savings:
                if saving.date_to >= new_data['date_from']:
                    saving.date_to = (datetime.strptime(
                        new_data['date_from'], "%Y-%m") - relativedelta(months=1)).strftime("%Y-%m")
                    saving.save()

            return self.post(request)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListView(APIView):

    def get(self, request):
        user = request.user
        return JsonResponse({
            'username': user.username,
            'email': user.email,
            'full_name': user.get_full_name()
        })


class PricesListView(APIView):

    def get_historical_prices(self, ticker, date_from):
        try:
            start_date = datetime.strptime(date_from, "%Y-%m")
            delta_months = (datetime.now().year - start_date.year) * 12 + datetime.now().month - start_date.month

            period = '1mo' if delta_months <= 1 else '3mo' if delta_months <= 3 else '6mo' if delta_months <= 6 else '1y' if delta_months <= 12 else '2y'
            stock = yf.Ticker(ticker)
            price_data = stock.history(period=period)
            
            if price_data.empty:return 0

            df = price_data.resample('ME').last()[['Close']]
            df.reset_index(inplace=True)

            historical_prices = {row['Date'].strftime('%Y-%m'): row['Close'] for _, row in df.iterrows()}

            return historical_prices
        except Exception:
            return 0
