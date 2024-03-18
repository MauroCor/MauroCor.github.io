from django.shortcuts import render, redirect

from .forms import FixedCostForm
from .models import FixedCost


def get_fixed_cost(request):
    form = FixedCostForm()
    return render(request, 'monthly.html', {'form': form})


def set_fixed_cost(request):
    if request.method == 'POST':
        form = FixedCostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fixed_cost_list')
    return render(request, 'monthly.html', {'form': form})


def fixed_cost_list(request):
    fixed_cost = FixedCost.objects.all()
    return render(request, 'monthly.html', {'Fixed cost': fixed_cost})
