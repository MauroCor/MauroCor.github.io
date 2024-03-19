from django import forms

from .models import Earning, FixedCost


class FixedCostForm(forms.ModelForm):
    class Meta:
        model = FixedCost
        fields = ['month', 'name', 'price']


class EarningForm(forms.ModelForm):
    class Meta:
        model = Earning
        fields = ['month', 'name', 'price']
