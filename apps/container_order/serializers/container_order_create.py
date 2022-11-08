from django.db.models import Q
from rest_framework import serializers

from apps.container_order.models import ContainerTypeOrder, ContainerOrder
from apps.core.models import Product, Station
from apps.order.models import Order


class ContainerPreliminaryCostCreateSerializer(serializers.Serializer):
    counterparty_id = serializers.IntegerField()
    category_id = serializers.IntegerField()
    preliminary_cost = serializers.DecimalField(decimal_places=2, max_digits=10)


# class ContainerExpanseCreateSerializer(serializers.Serializer):
#     container = serializers.CharField(max_length=100, allow_null=True, allow_blank=True)
#     counterparty_id = serializers.IntegerField()
#     category_id = serializers.IntegerField()
#     actual_cost = serializers.DecimalField(decimal_places=2, max_digits=10)


class CounterPartyOrderCreateSerializer(serializers.Serializer):
    category_id = serializers.IntegerField()
    counterparty_id = serializers.IntegerField()


class ContainerTypeOrderCreateSerializer(serializers.Serializer):
    agreed_rate = serializers.DecimalField(decimal_places=2, max_digits=10)
    quantity = serializers.IntegerField()
    container_type = serializers.ChoiceField(choices=ContainerTypeOrder.CONTAINER_TYPE_CHOICES)
    container_preliminary_costs = ContainerPreliminaryCostCreateSerializer(many=True)
    # expanses = ContainerExpanseCreateSerializer(many=True)


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


class ContainerOrderCreateSerializer(serializers.Serializer):
    order = OrderCreateSerializer()
    sending_type = serializers.ChoiceField(choices=ContainerOrder.SENDING_TYPE_CHOICES)
    product_id = serializers.IntegerField()

    def validate(self, data):
        if ContainerOrder.objects.filter(order__order_number=data['order']['order_number']).exists():
            raise serializers.ValidationError('Order number already exists')
        if not Station.objects.filter(Q(id=data['order']['departure_id']) or data['order']['destination_id']).exists():
            raise serializers.ValidationError('Departure or Destination station doesnt exist')
        if not Product.objects.filter(id=data['product_id']).exists():
            raise serializers.ValidationError('Product doesnt exist')
        return data

    def create(self, validated_data):
        order_data = validated_data.pop('order')
        base_order = Order.objects.create(**order_data)
        ContainerOrder.objects.create(order=base_order, **validated_data)

        return base_order
