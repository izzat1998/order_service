from django.db.models import Q
from rest_framework import serializers

from apps.core.models import Station, Product
from apps.order.models import WagonOrder, Order


class OrderCreateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    order_number = serializers.IntegerField()
    lot_number = serializers.CharField(max_length=255)
    date = serializers.DateField()
    position = serializers.ChoiceField(choices=Order.POSITION_CHOICES)
    type = serializers.ChoiceField(choices=Order.ORDER_TYPE_CHOICES)
    shipment_status = serializers.ChoiceField(choices=Order.SHIPMENT_STATUS_CHOICES)
    payment_status = serializers.ChoiceField(choices=Order.PAYMENT_STATUS_CHOICES)
    shipper = serializers.CharField(max_length=255)
    consignee = serializers.CharField(max_length=255)
    departure_id = serializers.IntegerField()
    destination_id = serializers.IntegerField()
    border_crossing = serializers.CharField(max_length=255)
    conditions_of_carriage = serializers.CharField()
    rolling_stock = serializers.CharField(max_length=255)
    departure_country = serializers.CharField(max_length=255)
    destination_country = serializers.CharField(max_length=255)
    comment = serializers.CharField(max_length=255)
    manager = serializers.IntegerField()
    customer = serializers.IntegerField()


class WagonOrderCreateSerializer(serializers.Serializer):
    order = OrderCreateSerializer()
    product_id = serializers.IntegerField()

    def validate(self, data):
        if WagonOrder.objects.filter(order__order_number=data['order']['order_number']).exists():
            raise serializers.ValidationError('Order number already exists')
        if not Station.objects.filter(Q(id=data['order']['departure_id']) or data['order']['destination_id']).exists():
            raise serializers.ValidationError('Departure or Destination station doesnt exist')
        if not Product.objects.filter(id=data['product_id']).exists():
            raise serializers.ValidationError('Product doesnt exist')
        return data

    def create(self, validated_data):
        order_data = validated_data.pop('order')
        base_order = Order.objects.create(**order_data)
        WagonOrder.objects.create(order=base_order, **validated_data)

        return base_order
