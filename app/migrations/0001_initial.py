# Generated by Django 5.0.3 on 2024-11-06 21:08

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CardSpend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('price', models.DecimalField(decimal_places=0, max_digits=9)),
                ('fees', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(36)])),
                ('init_month', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)])),
            ],
        ),
        migrations.CreateModel(
            name='FixedCost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('price', models.DecimalField(decimal_places=0, max_digits=9)),
                ('date_from', models.CharField(max_length=7, validators=[django.core.validators.RegexValidator(message='Format date should be YYYY-MM', regex='^\\d{4}-\\d{2}$')])),
                ('date_to', models.CharField(max_length=7, validators=[django.core.validators.RegexValidator(message='Format date should be YYYY-MM', regex='^\\d{4}-\\d{2}$')])),
            ],
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('price', models.DecimalField(decimal_places=0, max_digits=9)),
                ('date_from', models.CharField(max_length=7, validators=[django.core.validators.RegexValidator(message='Format date should be YYYY-MM', regex='^\\d{4}-\\d{2}$')])),
                ('date_to', models.CharField(max_length=7, validators=[django.core.validators.RegexValidator(message='Format date should be YYYY-MM', regex='^\\d{4}-\\d{2}$')])),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.CharField(max_length=3)),
                ('bills', models.CharField(max_length=10)),
                ('cash', models.CharField(max_length=10)),
                ('note', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='InstallmentPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('fee_value', models.DecimalField(decimal_places=0, max_digits=9)),
                ('month', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)])),
                ('fee_num', models.IntegerField()),
                ('card_spend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.cardspend')),
            ],
        ),
    ]
