from rest_framework import serializers

from apps.core.serializers import WagonSerializer
from apps.counterparty.serializers import CounterpartySerializer, CategorySerializer
from apps.order.models import Order


class WagonEmptyCounterPartyOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    category = CategorySerializer()
    counterparty = CounterpartySerializer()


class WagonEmptyActualCostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    actual_cost = serializers.DecimalField(max_digits=10, decimal_places=2)
    counterparty = WagonEmptyCounterPartyOrderSerializer()


class WagonEmptyExpanseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    wagon = WagonSerializer()
    actual_costs = WagonEmptyActualCostSerializer(many=True)
    agreed_rate = serializers.DecimalField(max_digits=10, decimal_places=2)


class StationSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100, read_only=True)
    code = serializers.CharField(max_length=100, read_only=True)
    railway_name = serializers.CharField(max_length=255, read_only=True)


class OrderSerializer(serializers.Serializer):
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
    counterparties = WagonEmptyCounterPartyOrderSerializer(many=True)


class PreliminaryCostSerializer(serializers.Serializer):
    counterparty_id = serializers.IntegerField()
    preliminary_cost = serializers.DecimalField(max_digits=10, decimal_places=2)


class WagonEmptyOrderSerializer(serializers.Serializer):
    order = OrderSerializer()
    wagon_empty_preliminary_costs = PreliminaryCostSerializer(many=True)
    agreed_rate = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField()
    expanses = WagonEmptyExpanseSerializer(many=True)
