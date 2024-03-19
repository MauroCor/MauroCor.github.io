from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class FixedCost(models.Model):
    month = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=1000000, decimal_places=0)


class Earning(models.Model):
    month = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=1000000, decimal_places=0)


class CardSpend(models.Model):
    name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=1000000, decimal_places=0)
    fees = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(36)])
    init_month = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])


class InstallmentPayment(models.Model):
    card_spend = models.ForeignKey(CardSpend, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    fee_value = models.DecimalField(max_digits=1000000, decimal_places=0)
    month = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])

    @staticmethod
    def generate_instalments(card_spend):
        for month in range(card_spend.init_month, card_spend.init_month + card_spend.fees):
            InstallmentPayment.objects.create(
                card_spend=card_spend,
                name=f"{card_spend.name} ({month - card_spend.init_month + 1}/{card_spend.fees})",
                fee_value=card_spend.price / card_spend.fees,
                month=month
            )
