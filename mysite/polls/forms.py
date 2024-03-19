from django import forms

from .models import Earning, FixedCost, CardSpend


class FixedCostForm(forms.ModelForm):
    class Meta:
        model = FixedCost
        fields = ['month', 'name', 'price']


class EarningForm(forms.ModelForm):
    class Meta:
        model = Earning
        fields = ['month', 'name', 'price']


class CardSpendForm(forms.ModelForm):
    class Meta:
        model = CardSpend
        fields = ['name', 'price', 'fees', 'init_month']
