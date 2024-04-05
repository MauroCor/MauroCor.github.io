from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class FixedCost(models.Model):
    month = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=9, decimal_places=0)


class Earning(models.Model):
    month = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=9, decimal_places=0)


class CardSpend(models.Model):
    name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=9, decimal_places=0)
    fees = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(36)])
    init_month = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])


class InstallmentPayment(models.Model):
    card_spend = models.ForeignKey(CardSpend, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
    fee_value = models.DecimalField(max_digits=9, decimal_places=0)
    month = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    fee_num = models.IntegerField()  # Agregamos el campo fee_num

    @staticmethod
    def generate_installments_payments(card_spend):
        for fee_num, month in enumerate(range(card_spend.init_month, card_spend.init_month + card_spend.fees), start=1):
            InstallmentPayment.objects.create(
                card_spend=card_spend,
                name=f"{card_spend.name}_{month}",
                fee_value=card_spend.price / card_spend.fees,
                month=month,
                fee_num=fee_num)
