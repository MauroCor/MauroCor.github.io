from django import forms
from .models import Gasto, Ingreso

class GastoForm(forms.ModelForm):
    class Meta:
        model = Gasto
        fields = ['fecha', 'concepto', 'monto']

class IngresoForm(forms.ModelForm):
    class Meta:
        model = Ingreso
        fields = ['fecha', 'concepto', 'monto']
