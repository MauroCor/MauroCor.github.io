from rest_framework import serializers
from datetime import datetime

from app.models import CardSpend, FixedCost, Income, Saving
from django.db.models import Q

class FixedCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = FixedCost
        fields = ('name', 'price', 'date_from', 'date_to', 'user', 'ccy')
        extra_kwargs = {
            'date_to': {'required': False, 'allow_null': True}
        }

    def validate(self, data):
        if self.context.get('request') and self.context['request'].method != 'PATCH':
            date_from = datetime.strptime(data.get('date_from'), "%Y-%m")
            date_to = data.get('date_to')

            if date_to:
                date_to = datetime.strptime(date_to, "%Y-%m")
            else:
                # Si date_to = null, asumir un año después de date_from
                date_to = date_from.replace(year=date_from.year + 1)
                data['date_to'] = date_to.strftime("%Y-%m")

            instance_id = self.instance.id if self.instance else None
            user_id = data.get('user')

            if self.context['request'].method != 'PUT':
                overlapping_costs = FixedCost.objects.filter(
                    user_id=user_id,
                    name=data['name'],
                ).exclude(id=instance_id).filter(
                    Q(date_from__lte=data['date_to']) & Q(
                        date_to__gte=data['date_from'])
                )

                if overlapping_costs.exists():
                    raise serializers.ValidationError(
                        f"'{data['name']}' already exist between these dates."
                    )
        return data


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ('name', 'price', 'date_from', 'date_to', 'user', 'ccy')
        extra_kwargs = {
            'date_to': {'required': False, 'allow_null': True}
        }

    def validate(self, data):
        if self.context.get('request') and self.context['request'].method != 'PATCH':
            date_from = datetime.strptime(data.get('date_from'), "%Y-%m")
            date_to = data.get('date_to')
            if date_to:
                date_to = datetime.strptime(date_to, "%Y-%m")
            else:
                # Si date_to = null, asumir un año después de date_from
                date_to = date_from.replace(year=date_from.year + 1)
                data['date_to'] = date_to.strftime("%Y-%m")

            instance_id = self.instance.id if self.instance else None
            user_id = data.get('user')

            if self.context['request'].method != 'PUT':
                overlapping_costs = Income.objects.filter(
                    user_id=user_id,
                    name=data['name'],
                ).exclude(id=instance_id).filter(
                    Q(date_from__lte=data['date_to']) & Q(
                        date_to__gte=data['date_from'])
                )

                if overlapping_costs.exists():
                    raise serializers.ValidationError(
                        f"'{data['name']}' already exist between these dates."
                    )
        return data


class CardSpendSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardSpend
        fields = ('id', 'name', 'price', 'fees', 'date_from', 'user')


class SavingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saving
        fields = ('id', 'name', 'type', 'invested', 'obtained',
                  'date_from', 'date_to', 'user', 'tna', 'qty', 'ccy', 'crypto')
        extra_kwargs = {
            'qty': {'required': False, 'allow_null': True},
            'tna': {'required': False, 'allow_null': True},
            'obtained': {'required': False, 'allow_null': True},
            'crypto': {'required': False, 'allow_null': True},
            'date_to': {'required': False, 'allow_null': True}
        }

    def validate(self, data):
        if self.context.get('request') and self.context['request'].method != 'PATCH':
            date_from = datetime.strptime(data.get('date_from'), "%Y-%m")
            date_to = data.get('date_to')
            if date_to:
                date_to = datetime.strptime(date_to, "%Y-%m")
            else:
                # Si date_to = null, asumir un año después de date_from
                date_to = date_from.replace(year=date_from.year + 1)
                data['date_to'] = date_to.strftime("%Y-%m")

            instance_id = self.instance.id if self.instance else None
            user_id = data.get('user')

            if self.context['request'].method != 'PUT':
                overlapping_costs = Saving.objects.filter(
                    user_id=user_id,
                    name=data['name'],
                ).exclude(id=instance_id).filter(
                    Q(date_from__lte=data['date_to']) & Q(
                        date_to__gte=data['date_from'])
                )

                if overlapping_costs.exists() and data['type'] != 'fijo':
                    raise serializers.ValidationError(
                        f"'{data['name']}' already exist between these dates."
                    )
        return data
