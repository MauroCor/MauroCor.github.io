from django.db.models import Sum
from django.shortcuts import render, redirect

from .forms import FixedCostForm, EarningForm, CardSpendForm
from .models import FixedCost, Earning, CardSpend, InstallmentPayment


def get_fixed_costs():
    fixed_costs = FixedCost.objects.all()
    outflow_by_month = FixedCost.objects.values('month').annotate(total_price=Sum('price'))
    return fixed_costs, outflow_by_month


def set_fixed_cost(request):
    if request.method == 'POST':
        form = FixedCostForm(request.POST)
        if form.is_valid():
            new_fixed_cost = form.save(commit=False)
            existing_fixed_cost = FixedCost.objects.filter(month=new_fixed_cost.month, name=new_fixed_cost.name).first()
            if existing_fixed_cost:
                existing_fixed_cost.price = new_fixed_cost.price
                for month in range(existing_fixed_cost.month, 13):
                    FixedCost.objects.update_or_create(
                        month=month,
                        name=existing_fixed_cost.name,
                        defaults={'price': existing_fixed_cost.price}
                    )
            else:
                for month in range(new_fixed_cost.month, 13):
                    FixedCost.objects.update_or_create(
                        month=month,
                        name=new_fixed_cost.name,
                        price=new_fixed_cost.price
                    )
            return redirect(gets_monthly)
    else:
        form = FixedCostForm()
    return render(request, 'monthly.html', {'form': form})


def get_earnings():
    earnings = Earning.objects.all()
    inflow_by_month = Earning.objects.values('month').annotate(total_price=Sum('price'))
    return earnings, inflow_by_month


def set_earning(request):
    if request.method == 'POST':
        form = EarningForm(request.POST)
        if form.is_valid():
            new_earning = form.save(commit=False)
            existing_earnings = Earning.objects.filter(month=new_earning.month, name=new_earning.name).first()
            if existing_earnings:
                existing_earnings.price = new_earning.price
                for month in range(existing_earnings.month, 13):
                    Earning.objects.update_or_create(
                        month=month,
                        name=existing_earnings.name,
                        defaults={'price': existing_earnings.price}
                    )
            else:
                for month in range(new_earning.month, 13):
                    Earning.objects.update_or_create(
                        month=month,
                        name=new_earning.name,
                        price=new_earning.price
                    )
            return redirect(gets_monthly)
    else:
        form = EarningForm()
    return render(request, 'monthly.html', {'form': form})


def get_balance():
    balance_by_month = []
    for month in range(1, 13):
        outflow_total = FixedCost.objects.filter(month=month).aggregate(total_outflow=Sum('price'))[
                            'total_outflow'] or 0
        inflow_total = Earning.objects.filter(month=month).aggregate(total_inflow=Sum('price'))['total_inflow'] or 0
        balance = inflow_total - outflow_total
        balance_by_month.append({'month': month, 'balance': balance})
    return balance_by_month


def gets_monthly(request):
    fixed_costs, outflow_by_month = get_fixed_costs()
    earnings, inflow_by_month = get_earnings()
    balance_by_month = get_balance()
    return render(request, 'monthly.html',
                  {'fixed_costs': fixed_costs,
                   'outflow_by_month': outflow_by_month,
                   'earnings': earnings,
                   'inflow_by_month': inflow_by_month,
                   'balance_by_month': balance_by_month})


def get_card_spend():
    return CardSpend.objects.all(), InstallmentPayment.objects.all()


def set_card_spend(request):
    if request.method == 'POST':
        form = CardSpendForm(request.POST)
        if form.is_valid():
            card_spend = form.save()  # Guarda el CardSpend
            InstallmentPayment.generate_instalments(card_spend)  # Genera los pagos a plazos
            return redirect(gets_card)
    else:
        form = CardSpendForm()
    return render(request, 'card.html', {'form': form})


def get_card_balance():
    total_card_spend_by_month = []
    for month in range(1, 13):
        total_by_month = InstallmentPayment.objects.filter(month=month).aggregate(total_by_month=Sum('fee_value'))[
                               'total_by_month'] or 0
        total_card_spend_by_month.append({'month': month, 'total': total_by_month})
    return total_card_spend_by_month


def gets_card(request):
    card_spends, installment_payments = get_card_spend()
    total_card_spend_by_month = get_card_balance()
    return render(request, 'card.html',
                  {'card_spends': card_spends,
                   'installment_payments': installment_payments,
                   'total_card_spend_by_month': total_card_spend_by_month})
