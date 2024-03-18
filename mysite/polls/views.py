from django.shortcuts import render, redirect

from .forms import FixedCostForm
from .models import FixedCost


def get_fixed_costs(request):
    fixed_costs = FixedCost.objects.all()
    return render(request, 'monthly.html', {'fixed_costs': fixed_costs})


def set_fixed_cost(request):
    if request.method == 'POST':
        form = FixedCostForm(request.POST)
        if form.is_valid():
            new_fixed_cost = form.save(commit=False)
            existing_fixed_cost = FixedCost.objects.filter(month=new_fixed_cost.month, name=new_fixed_cost.name).first()
            if existing_fixed_cost:
                print("Si existe")
                existing_fixed_cost.price = new_fixed_cost.price
                for month in range(existing_fixed_cost.month, 13):
                    FixedCost.objects.update_or_create(
                        month=month,
                        name=existing_fixed_cost.name,
                        defaults={'price': existing_fixed_cost.price}
                    )
            else:
                print("No existe")
                for month in range(new_fixed_cost.month, 13):
                    FixedCost.objects.update_or_create(
                        month=month,
                        name=new_fixed_cost.name,
                        price=new_fixed_cost.price
                    )
            return redirect(get_fixed_costs)
    else:
        form = FixedCostForm()
    return render(request, 'monthly.html', {'form': form})
