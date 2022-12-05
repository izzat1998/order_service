from rest_framework import serializers


from apps.core.serializers import WagonSerializer
from apps.counterparty.serializers import CategorySerializer, CounterpartySerializer
from apps.order.models import Order


class WagonCounterPartyOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    category = CategorySerializer()
    counterparty = CounterpartySerializer()


class WagonActualCost(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    counterparty = WagonCounterPartyOrderSerializer()
    actual_cost = serializers.DecimalField(max_digits=10, decimal_places=2)


class WagonExpanseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    agreed_rate_per_tonn = serializers.DecimalField(max_digits=10, decimal_places=2)
    actual_weight = serializers.IntegerField()
    wagon = WagonSerializer()
    actual_costs = WagonActualCost(many=True)


class WagonPreliminaryCostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    counterparty = WagonCounterPartyOrderSerializer()
    preliminary_cost = serializers.DecimalField(max_digits=10, decimal_places=2)


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
    counterparties = WagonCounterPartyOrderSerializer(many=True)


class WagonOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    order = OrderSerializer()
    product = ProductSerializer()
    wagon_preliminary_costs = WagonPreliminaryCostSerializer(many=True)
    expanses = WagonExpanseSerializer(many=True)
