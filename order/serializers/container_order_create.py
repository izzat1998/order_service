from django.db.models import Q
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from core.models import Product, Station
from order.models import Order, ContainerOrder, ContainerTypeOrder, CounterPartyOrder, ContainerPreliminaryCost

from order.serializers.serializers import StationSerializer


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
    counterparties = CounterPartyOrderCreateSerializer(many=True)


class ContainerOrderCreateSerializer(serializers.Serializer):
    order = OrderCreateSerializer()
    container_types = ContainerTypeOrderCreateSerializer(many=True)
    sending_type = serializers.ChoiceField(choices=ContainerOrder.SENDING_TYPE_CHOICES)
    product_id = serializers.IntegerField()

    def validate(self, data):
        if ContainerOrder.objects.filter(order__order_number=data['order']['order_number']).exists():
            raise serializers.ValidationError('Order number already exists')
        if not Station.objects.filter(Q(id=data['order']['departure_id']) or data['order']['destination_id']).exists():
            raise serializers.ValidationError('Departure or Destination station doesnt exist')
        if not Product.objects.filter(id=data['product_id']):
            raise serializers.ValidationError('Product doesnt exist')
        return data

    def create(self, validated_data):

        order_data = validated_data.pop('order')
        counterparty_data = order_data.pop('counterparties')
        container_type_data = validated_data.pop('container_types')

        base_order = Order.objects.create(**order_data)
        order = ContainerOrder.objects.create(order=base_order, **validated_data)
        counterparty = CounterPartyOrderCreateSerializer(data=counterparty_data, many=True)
        if counterparty.is_valid(raise_exception=True):
            for counterparty in counterparty.data:
                CounterPartyOrder.objects.create(**counterparty, order=base_order)
        container_type = ContainerTypeOrderCreateSerializer(data=container_type_data, many=True)
        if container_type.is_valid(raise_exception=True):
            for container_type in container_type.data:
                container_preliminary_cost_data = container_type.pop('container_preliminary_costs')

                container_type = ContainerTypeOrder.objects.create(**container_type, order=order)
                container_preliminary_cost = ContainerPreliminaryCostCreateSerializer(
                    data=container_preliminary_cost_data, many=True)
                if container_preliminary_cost.is_valid(raise_exception=True):

                    for preliminary_cost in container_preliminary_cost.data:
                        counterparty = get_object_or_404(CounterPartyOrder, order=base_order,
                                                         counterparty_id=preliminary_cost[
                                                             'counterparty_id'],
                                                         category_id=preliminary_cost['category_id']
                                                         )
                        ContainerPreliminaryCost.objects.create(counterparty=counterparty,
                                                                container_type=container_type,
                                                                preliminary_cost=preliminary_cost['preliminary_cost']
                                                                )
        return base_order
