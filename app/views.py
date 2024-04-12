from django.contrib import messages
from django.db import transaction
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .forms import FixedCostForm, EarningForm, CardSpendForm, InvestForm
from .models import FixedCost, Earning, CardSpend, InstallmentPayment, Invest


# Fixed cost section
def get_fixed_costs():
    fixed_costs = FixedCost.objects.all()
    monthly_outflow = FixedCost.objects.values('month').annotate(result=Sum('price'))
    return fixed_costs, monthly_outflow


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
                        price=new_fixed_cost.price)
            return redirect(gets_monthly)
    else:
        form = FixedCostForm()
    return render(request, 'monthly.html', {'form': form})


@transaction.atomic
def edit_fixed_cost(request, old_name, new_name):
    try:
        fixed_costs = FixedCost.objects.filter(name=old_name)
        if FixedCost.objects.filter(name=new_name).exists():
            return JsonResponse({'success': False, 'err_msg': f"'{new_name}' already exist."}, status=400)
        for fixed_cost in fixed_costs:
            fixed_cost.name = new_name
            fixed_cost.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'err_msg': str(e)}, status=500)


def delete_fixed_cost(request, fixed_cost_name):
    FixedCost.objects.filter(name=fixed_cost_name).delete()
    return redirect(gets_monthly)


# Earning section
def get_earnings():
    earnings = Earning.objects.all()
    monthly_inflow = Earning.objects.values('month').annotate(result=Sum('price'))
    return earnings, monthly_inflow


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
                        price=new_earning.price)
            return redirect(gets_monthly)
    else:
        form = EarningForm()
    return render(request, 'monthly.html', {'form': form})


@transaction.atomic
def edit_earning(request, old_name, new_name):
    try:
        earnings = Earning.objects.filter(name=old_name)
        if Earning.objects.filter(name=new_name).exists():
            return JsonResponse({'success': False, 'err_msg': f"'{new_name}' already exist."}, status=400)
        for earning in earnings:
            earning.name = new_name
            earning.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'err_msg': str(e)}, status=500)


def delete_earning(request, earning_name):
    Earning.objects.filter(name=earning_name).delete()
    return redirect(gets_monthly)


def set_invest(request):
    if request.method == 'POST':
        form = InvestForm(request.POST)
        if form.is_valid():
            new_invest = form.save(commit=False)
            existing_invest, created = Invest.objects.get_or_create(month=new_invest.month)
            existing_invest.vwallet = new_invest.vwallet
            existing_invest.total = new_invest.total
            existing_invest.note = new_invest.note
            existing_invest.save()
            return redirect(gets_monthly)
    else:
        form = InvestForm()
    return render(request, 'monthly.html', {'form': form})


def get_balance():
    monthly_balance = []
    for month in range(1, 13):
        monthly_outflow = FixedCost.objects.filter(month=month).aggregate(monthly_outflow=Sum('price'))[
                              'monthly_outflow'] or 0
        monthly_inflow = Earning.objects.filter(month=month).aggregate(monthly_inflow=Sum('price'))[
                             'monthly_inflow'] or 0
        balance = monthly_inflow - monthly_outflow
        monthly_balance.append({'month': month, 'result': balance})
    return monthly_balance


def gets_monthly(request):
    fixed_costs, monthly_outflow = get_fixed_costs()
    earnings, monthly_inflow = get_earnings()
    monthly_balance = get_balance()
    unique_fixed_cost_names = set(fixed_cost.name for fixed_cost in fixed_costs)
    unique_earnings_names = set(earnings.name for earnings in earnings)
    months = list(range(1, 13))
    invests = Invest.objects.all()
    return render(request, 'monthly.html',
                  {'months': months,
                   'fixed_costs': fixed_costs,
                   'monthly_outflow': monthly_outflow,
                   'unique_fixed_cost_names': unique_fixed_cost_names,
                   'earnings': earnings,
                   'monthly_inflow': monthly_inflow,
                   'unique_earnings_names': unique_earnings_names,
                   'invests': invests,
                   'monthly_balance': monthly_balance})


# Card spend section
def get_card_spend():
    return CardSpend.objects.all(), InstallmentPayment.objects.all()


@transaction.atomic
def set_card_spend(request):
    if request.method == 'POST':
        form = CardSpendForm(request.POST)
        if form.is_valid():
            new_name = form.cleaned_data['name']
            if CardSpend.objects.filter(name=new_name).exists():
                messages.error(request, f"'{new_name}' already exists.")
                return redirect(gets_card)
            card_spend = form.save()
            InstallmentPayment.generate_installments_payments(card_spend)
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
    # Set CreditCard(FixedCost)=total_card_spend_by_month
    for month_total in total_card_spend_by_month:
        FixedCost.objects.update_or_create(
            month=month_total['month'],
            name='CreditCard',
            defaults={'price': month_total['total']})
    months = list(range(1, 13))
    return render(request, 'card.html',
                  {'months': months,
                   'card_spends': card_spends,
                   'installment_payments': installment_payments,
                   'total_card_spend_by_month': total_card_spend_by_month})


@transaction.atomic
def edit_card_spend(request, old_name, new_name):
    try:
        card_spends = CardSpend.objects.filter(name=old_name)
        if card_spends.count() != 1:
            return JsonResponse({'success': False, 'err_msg': f"'{old_name}' duplicated ."}, status=404)
        if CardSpend.objects.filter(name=new_name).exists():
            return JsonResponse({'success': False, 'err_msg': f"'{new_name}' already exist."}, status=400)
        card_spend = card_spends.first()
        card_spend.name = new_name
        card_spend.save()
        installment_payments = InstallmentPayment.objects.filter(card_spend=card_spend)
        for installment_payment in installment_payments:
            installment_payment.name = f"{new_name}_{installment_payment.month}"
            installment_payment.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'err_msg': str(e)}, status=500)


def delete_card_spend(request, card_spend_id):
    card_spend = CardSpend.objects.get(pk=card_spend_id)
    card_spend.delete()
    return redirect(gets_card)


# Home section
def home(request):
    return render(request, 'home.html')
