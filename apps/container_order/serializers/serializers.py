from django.db.models import Sum
from rest_framework import serializers

from apps.container_order.models import ContainerTypeOrder, ContainerOrder, ContainerActualCost
from apps.core.serializers import ContainerSerializer
from apps.counterparty.serializers import CategorySerializer, CounterpartySerializer
from apps.order.models import Order


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


class CounterPartyOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    category = CategorySerializer()
    counterparty = CounterpartySerializer()


class CounterPartyOrderTotalExpanseSerializer(serializers.Serializer):
    total_expanses = serializers.SerializerMethodField('_get_total_expanses')

    id = serializers.IntegerField(read_only=True)
    category = CategorySerializer()
    counterparty = CounterpartySerializer()

    def _get_total_expanses(self, obj):
        return ContainerActualCost.objects.filter(counterparty_id=obj.id).aggregate(total=Sum('actual_cost'))['total']


class ContainerActualCostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    counterparty_id = serializers.IntegerField()
    actual_cost = serializers.DecimalField(decimal_places=2, max_digits=10)


class ContainerExpanseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    container = ContainerSerializer()
    actual_costs = ContainerActualCostSerializer(many=True)


class ContainerPreliminaryCost(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    counterparty = CounterPartyOrderSerializer()
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
    counterparties = CounterPartyOrderTotalExpanseSerializer(many=True)


class ContainerOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    order = OrderSerializer()
    sending_type = serializers.ChoiceField(choices=ContainerOrder.SENDING_TYPE_CHOICES)
    product = ProductSerializer()
    container_types = ContainerTypeOrderSerializer(many=True)
