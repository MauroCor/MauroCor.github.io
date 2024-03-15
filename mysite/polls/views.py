from django.shortcuts import render, redirect

from .forms import GastoForm, IngresoForm
from .models import Gasto, Ingreso


def lista_gastos(request):
    gastos = Gasto.objects.all()
    return render(request, 'lista_gastos.html', {'gastos': gastos})


def agregar_gasto(request):
    if request.method == 'POST':
        form = GastoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_gastos')
    else:
        form = GastoForm()
    return render(request, 'agregar_gasto.html', {'form': form})


def lista_ingresos(request):
    ingresos = Ingreso.objects.all()
    return render(request, 'lista_ingresos.html', {'ingresos': ingresos})


def agregar_ingreso(request):
    if request.method == 'POST':
        form = IngresoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_ingresos')
    else:
        form = IngresoForm()
    return render(request, 'agregar_ingreso.html', {'form': form})
