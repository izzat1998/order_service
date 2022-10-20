from rest_framework import serializers
from rest_framework.reverse import reverse

from counterparty.serializers import CategorySerializer, CounterpartySerializer
from order.models import ContainerOrder, Order, ContainerTypeOrder


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    hc_code = serializers.IntegerField(read_only=True)
    etcng_code = serializers.IntegerField(read_only=True)


class StationSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100, read_only=True)
    code = serializers.CharField(max_length=100, read_only=True)
    railway_name = serializers.CharField(max_length=255, read_only=True)


class CounterPartyOrder(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    category = CategorySerializer()
    counterparty = CounterpartySerializer()


class ContainerSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, read_only=True)


class ContainerExpanseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    container = ContainerSerializer()
    counterparty = CounterPartyOrder()
    actual_cost = serializers.DecimalField(decimal_places=2, max_digits=10)


class ContainerPreliminaryCost(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    counterparty = CounterPartyOrder()
    preliminary_cost = serializers.DecimalField(decimal_places=2, max_digits=10)


class ContainerTypeOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    agreed_rate = serializers.DecimalField(decimal_places=2, max_digits=10)
    quantity = serializers.IntegerField()
    container_type = serializers.ChoiceField(choices=ContainerTypeOrder.CONTAINER_TYPE_CHOICES)
    container_preliminary_costs = ContainerPreliminaryCost(many=True)
    expanses = ContainerExpanseSerializer(many=True)


class OrderSerializer(serializers.Serializer):

    order_number = serializers.IntegerField()
    lot_number = serializers.CharField(max_length=255)
    date = serializers.DateField()
    position = serializers.ChoiceField(choices=Order.POSITION_CHOICES)
    type = serializers.ChoiceField(choices=Order.ORDER_TYPE_CHOICES)
    shipment_status = serializers.ChoiceField(choices=Order.SHIPMENT_STATUS_CHOICES)
    payment_status = serializers.ChoiceField(choices=Order.PAYMENT_STATUS_CHOICES)
    shipper = serializers.CharField(max_length=255)
    consignee = serializers.CharField(max_length=255)
    departure = StationSerializer()
    destination = StationSerializer()
    border_crossing = serializers.CharField(max_length=255)
    conditions_of_carriage = serializers.CharField()
    rolling_stock = serializers.CharField(max_length=255)
    departure_country = serializers.CharField(max_length=255)
    destination_country = serializers.CharField(max_length=255)
    comment = serializers.CharField(max_length=255)
    manager = serializers.IntegerField()
    customer = serializers.IntegerField()
    counterparties = CounterPartyOrder(many=True)


class ContainerOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    order = OrderSerializer()
    sending_type = serializers.ChoiceField(choices=ContainerOrder.SENDING_TYPE_CHOICES)
    product = ProductSerializer()
    container_types = ContainerTypeOrderSerializer(many=True)
