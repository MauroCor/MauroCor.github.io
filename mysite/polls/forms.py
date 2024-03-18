from django import forms

from .models import Ingreso, FixedCost


class FixedCostForm(forms.ModelForm):
    class Meta:
        model = FixedCost
        fields = ['month', 'name', 'price']


class IngresoForm(forms.ModelForm):
    class Meta:
        model = Ingreso
        fields = ['fecha', 'concepto', 'monto']
