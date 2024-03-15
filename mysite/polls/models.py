from django.contrib.auth.models import User
from django.db import models


class Gasto(models.Model):
    fecha = models.DateField()
    concepto = models.CharField(max_length=100)
    monto = models.DecimalField(max_digits=10, decimal_places=2)


class Ingreso(models.Model):
    fecha = models.DateField()
    concepto = models.CharField(max_length=100)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
