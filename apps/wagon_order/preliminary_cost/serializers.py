from rest_framework import serializers

from apps.order.models import WagonOrder
from ..models import WagonPreliminaryCost


class WagonPreliminaryCostCreateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    counterparty_id = serializers.IntegerField()
    preliminary_cost = serializers.DecimalField(max_digits=10, decimal_places=2)
    order_number = serializers.IntegerField(source="order.order.order_number")

    def create(self, validated_data):
        order_number = validated_data.pop("order").pop("order").pop("order_number")
        wagon_order = WagonOrder.objects.filter(
            order__order_number=order_number
        ).first()
        return WagonPreliminaryCost.objects.create(**validated_data, order=wagon_order)


class WagonPreliminaryCostUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    counterparty_id = serializers.IntegerField(read_only=True)
    preliminary_cost = serializers.DecimalField(max_digits=10, decimal_places=2)

    def update(self, instance, validated_data):
        instance.preliminary_cost = validated_data.get("preliminary_cost")
        instance.save()
        return instance
