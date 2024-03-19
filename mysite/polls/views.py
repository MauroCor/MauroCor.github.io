from django.db.models import Sum
from django.shortcuts import render, redirect

from .forms import FixedCostForm, EarningForm
from .models import FixedCost, Earning


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
            return redirect(gets)
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
            new_earnings = form.save(commit=False)
            existing_earnings = Earning.objects.filter(month=new_earnings.month, name=new_earnings.name).first()
            if existing_earnings:
                existing_earnings.price = new_earnings.price
                for month in range(existing_earnings.month, 13):
                    Earning.objects.update_or_create(
                        month=month,
                        name=existing_earnings.name,
                        defaults={'price': existing_earnings.price}
                    )
            else:
                for month in range(new_earnings.month, 13):
                    Earning.objects.update_or_create(
                        month=month,
                        name=new_earnings.name,
                        price=new_earnings.price
                    )
            return redirect(gets)
    else:
        form = EarningForm()
    return render(request, 'monthly.html', {'form': form})


def get_balance():
    balance_by_month = []
    for month in range(1, 13):
        outflow_total = FixedCost.objects.filter(month=month).aggregate(total_outflow=Sum('price'))['total_outflow'] or 0
        inflow_total = Earning.objects.filter(month=month).aggregate(total_inflow=Sum('price'))['total_inflow'] or 0
        balance = inflow_total - outflow_total
        balance_by_month.append({'month': month, 'balance': balance})
    return balance_by_month


def gets(request):
    fixed_costs, outflow_by_month = get_fixed_costs()
    earnings, inflow_by_month = get_earnings()
    balance_by_month = get_balance()
    return render(request, 'monthly.html',
                  {'fixed_costs': fixed_costs,
                   'outflow_by_month': outflow_by_month,
                   'earnings': earnings,
                   'inflow_by_month': inflow_by_month,
                   'balance_by_month': balance_by_month})
