from rest_framework import serializers
from datetime import datetime

from app.models import CardSpend, FixedCost, Income, Saving


class FixedCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = FixedCost
        fields = ('name', 'price', 'date_from', 'date_to', 'user')
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
                    date_from__lte=date_to,
                    date_to__gte=date_from
                ).exclude(id=instance_id)

                if overlapping_costs.exists():
                    raise serializers.ValidationError(
                        f"'{data['name']}' already exist between these dates."
                    )
        return data


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ('name', 'price', 'date_from', 'date_to', 'user')
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
                    date_from__lte=date_to,
                    date_to__gte=date_from
                ).exclude(id=instance_id)

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
                  'date_from', 'date_to', 'user', 'tna')
        extra_kwargs = {
            'tna': {'required': False, 'allow_null': True},
            'obtained': {'required': False, 'allow_null': True},
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

        return data
