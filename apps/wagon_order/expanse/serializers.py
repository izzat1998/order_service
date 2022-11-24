from rest_framework import serializers

from apps.core.models import Wagon
from apps.order.models import WagonOrder
from apps.wagon_order.models import WagonExpanse, WagonActualCost


class WagonActualCostCreateSerializer(serializers.Serializer):
    counterparty_id = serializers.IntegerField()
    actual_cost = serializers.DecimalField(max_digits=10, decimal_places=2)


class WagonExpanseCreateSerializer(serializers.Serializer):
    order_number = serializers.IntegerField(source='order.order.order_number')
    actual_weight = serializers.IntegerField(default=60)
    actual_costs = WagonActualCostCreateSerializer(many=True)

    def create(self, validated_data):
        order_number = validated_data.pop('order').pop('order').pop('order_number')
        wagon_order = WagonOrder.objects.filter(order__order_number=order_number).first()
        expanse_wagon = WagonExpanse.objects.create(order=wagon_order)

        for expanse in validated_data.pop('actual_costs'):
            WagonActualCost.objects.create(
                counterparty_id=expanse.pop('counterparty_id'),
                actual_cost=expanse.pop('actual_cost'),
                wagon_expanse=expanse_wagon
            )
        return expanse_wagon


class WagonExpanseUpdateSerializer(serializers.Serializer):
    actual_weight = serializers.IntegerField(default=60)
    agreed_rate_per_tonn = serializers.DecimalField(decimal_places=2, max_digits=10)
    wagon_name = serializers.CharField(source='wagon.name')

