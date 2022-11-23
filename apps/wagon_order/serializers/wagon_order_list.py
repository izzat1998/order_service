from rest_framework import serializers

from apps.order.models import Order
from apps.wagon_order.serializers.serializers import StationSerializer, ProductSerializer


class OrderListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    order_number = serializers.IntegerField(read_only=True)
    lot_number = serializers.CharField(read_only=True)
    date = serializers.DateField(read_only=True)
    position = serializers.ChoiceField(source='get_position_display', choices=Order.POSITION_CHOICES, read_only=True)
    type = serializers.ChoiceField(source='get_type_display', choices=Order.ORDER_TYPE_CHOICES, read_only=True)
    shipment_status = serializers.ChoiceField(source='get_shipment_status_display',
                                              choices=Order.SHIPMENT_STATUS_CHOICES, read_only=True)
    payment_status = serializers.ChoiceField(source='get_payment_status_display', choices=Order.PAYMENT_STATUS_CHOICES,
                                             read_only=True)
    shipper = serializers.CharField(max_length=255, read_only=True)
    consignee = serializers.CharField(max_length=255, read_only=True)
    departure = StationSerializer(read_only=True)
    destination = StationSerializer(read_only=True)
    border_crossing = serializers.CharField(max_length=255, read_only=True)
    conditions_of_carriage = serializers.CharField(read_only=True)
    rolling_stock = serializers.CharField(max_length=255, read_only=True)
    departure_country = serializers.CharField(max_length=255, read_only=True)
    destination_country = serializers.CharField(max_length=255, read_only=True)
    comment = serializers.CharField(max_length=255, read_only=True)
    manager = serializers.IntegerField(read_only=True)
    customer = serializers.IntegerField(read_only=True)


class WagonOrderListSerializer(serializers.Serializer):
    order = OrderListSerializer()
    product = ProductSerializer()
    agreed_rate_per_tonn = serializers.DecimalField(max_digits=10, decimal_places=2)
    weight = serializers.IntegerField()
    quantity = serializers.IntegerField()
