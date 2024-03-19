from django.contrib import admin
from .models import FixedCost, Earning, CardSpend

admin.site.register(FixedCost)
admin.site.register(Earning)
admin.site.register(CardSpend)
