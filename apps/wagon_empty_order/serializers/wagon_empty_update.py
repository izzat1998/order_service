from django.db.models import Q
from rest_framework import serializers

from apps.core.models import Station
from apps.order.models import Order


class OrderUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    lot_number = serializers.CharField(
        max_length=255, allow_blank=True, allow_null=True
    )
    date = serializers.DateField()
    position = serializers.ChoiceField(choices=Order.POSITION_CHOICES)
    type = serializers.ChoiceField(choices=Order.ORDER_TYPE_CHOICES)
    shipment_status = serializers.ChoiceField(choices=Order.SHIPMENT_STATUS_CHOICES)
    payment_status = serializers.ChoiceField(choices=Order.PAYMENT_STATUS_CHOICES)
    shipper = serializers.CharField(max_length=255, allow_blank=True, allow_null=True)
    consignee = serializers.CharField(max_length=255, allow_blank=True, allow_null=True)
    departure_id = serializers.IntegerField()
    destination_id = serializers.IntegerField()
    border_crossing = serializers.CharField(
        max_length=255, allow_blank=True, allow_null=True
    )
    conditions_of_carriage = serializers.CharField(allow_blank=True, allow_null=True)
    rolling_stock = serializers.CharField(max_length=255, allow_blank=True)
    departure_country = serializers.CharField(
        max_length=255, allow_blank=True, allow_null=True
    )
    destination_country = serializers.CharField(
        max_length=255, allow_blank=True, allow_null=True
    )
    comment = serializers.CharField(max_length=255, allow_blank=True, allow_null=True)
    manager = serializers.IntegerField()
    customer = serializers.IntegerField()


class WagonEmptyOrderUpdateSerializer(serializers.Serializer):
    order = OrderUpdateSerializer()
    quantity = serializers.IntegerField()

    def validate(self, data):
        if not Station.objects.filter(
                Q(id=data["order"]["departure_id"]) or data["order"]["destination_id"]
        ).exists():
            raise serializers.ValidationError(
                "Departure or Destination station doesnt exist"
            )
        return data

    def update(self, instance, validated_data):
        order_data = validated_data.pop("order")
        instance.order.lot_number = order_data.pop("lot_number")
        instance.order.position = order_data.pop("position")
        instance.order.date = order_data.pop("date")
        instance.order.type = order_data.pop("type")
        instance.order.shipment_status = order_data.pop("shipment_status")
        instance.order.payment_status = order_data.pop("payment_status")
        instance.order.shipper = order_data.pop("shipper")
        instance.order.consignee = order_data.pop("consignee")
        instance.order.departure_id = order_data.pop("departure_id")
        instance.order.destination_id = order_data.pop("destination_id")
        instance.order.border_crossing = order_data.pop("border_crossing")
        instance.order.conditions_of_carriage = order_data.pop("conditions_of_carriage")
        instance.order.rolling_stock = order_data.pop("rolling_stock")
        instance.order.departure_country = order_data.pop("departure_country")
        instance.order.destination_country = order_data.pop("destination_country")
        instance.order.comment = order_data.pop("comment")
        instance.order.manager = order_data.pop("manager")
        instance.order.customer = order_data.pop("customer")
        instance.order.save()
        instance.save()
        return instance
