from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


class FixedCost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=9, decimal_places=0)
    ccy = models.CharField(max_length=4)
    date_from = models.CharField(
        max_length=7,
        validators=[
            RegexValidator(regex=r'^\d{4}-\d{2}$', message='Format date should be YYYY-MM'),
        ]
    )
    date_to = models.CharField(
        max_length=7,
        validators=[
            RegexValidator(regex=r'^\d{4}-\d{2}$', message='Format date should be YYYY-MM'),
        ]
    )


class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=9, decimal_places=0)
    ccy = models.CharField(max_length=4)
    date_from = models.CharField(
        max_length=7,
        validators=[
            RegexValidator(regex=r'^\d{4}-\d{2}$', message='Format date should be YYYY-MM'),
        ]
    )
    date_to = models.CharField(
        max_length=7,
        validators=[
            RegexValidator(regex=r'^\d{4}-\d{2}$', message='Format date should be YYYY-MM'),
        ]
    )


class CardSpend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=9, decimal_places=0)
    fees = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(36)])
    date_from = models.CharField(
        max_length=7,
        validators=[
            RegexValidator(regex=r'^\d{4}-\d{2}$', message='Format date should be YYYY-MM'),
        ]
    )

class Saving(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    type = models.CharField(max_length=4)
    invested = models.DecimalField(max_digits=9, decimal_places=0)
    ccy = models.CharField(max_length=4)
    obtained = models.DecimalField(max_digits=9, decimal_places=0, null=True, blank=True)
    date_from = models.CharField(
        max_length=7,
        validators=[
            RegexValidator(regex=r'^\d{4}-\d{2}$', message='Format date should be YYYY-MM'),
        ]
    )
    date_to = models.CharField(
        max_length=7,
        validators=[
            RegexValidator(regex=r'^\d{4}-\d{2}$', message='Format date should be YYYY-MM'),
        ]
    )
    tna = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    qty = models.DecimalField(max_digits=15, decimal_places=9, null=True, blank=True)
    crypto = models.BooleanField(null=True, blank=True)