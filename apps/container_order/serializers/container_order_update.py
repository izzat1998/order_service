from django.db.models import Q
from rest_framework import serializers

from apps.container_order.models import ContainerTypeOrder, ContainerOrder
from apps.core.models import Station, Product
from apps.order.models import Order


class ContainerPreliminaryCostUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    preliminary_cost = serializers.DecimalField(decimal_places=2, max_digits=10)


class ContainerTypeOrderUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    agreed_rate = serializers.DecimalField(decimal_places=2, max_digits=10)
    container_type = serializers.ChoiceField(choices=ContainerTypeOrder.CONTAINER_TYPE_CHOICES)
    container_preliminary_costs = ContainerPreliminaryCostUpdateSerializer(many=True)
    # expanses = ContainerExpanseCreateSerializer(many=True)


class OrderUpdateSerializer(serializers.Serializer):
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


class ContainerOrderUpdateSerializer(serializers.Serializer):
    order = OrderUpdateSerializer()
    sending_type = serializers.ChoiceField(choices=ContainerOrder.SENDING_TYPE_CHOICES)
    product_id = serializers.IntegerField()

    def validate(self, data):

        if not Station.objects.filter(Q(id=data['order']['departure_id']) or data['order']['destination_id']).exists():
            raise serializers.ValidationError('Departure or Destination station doesnt exist')
        if not Product.objects.filter(id=data['product_id']):
            raise serializers.ValidationError('Product doesnt exist')
        return data

    def update(self, instance, validated_data):
        order_data = validated_data.pop('order')
        instance.order.lot_number = order_data.pop('lot_number')
        instance.order.position = order_data.pop('position')
        instance.order.type = order_data.pop('type')
        instance.order.shipment_status = order_data.pop('shipment_status')
        instance.order.payment_status = order_data.pop('payment_status')
        instance.order.shipper = order_data.pop('shipper')
        instance.order.consignee = order_data.pop('consignee')
        instance.order.departure_id = order_data.pop('departure_id')
        instance.order.destination_id = order_data.pop('destination_id')
        instance.order.border_crossing = order_data.pop('border_crossing')
        instance.order.conditions_of_carriage = order_data.pop('conditions_of_carriage')
        instance.order.rolling_stock = order_data.pop('rolling_stock')
        instance.order.departure_country = order_data.pop('departure_country')
        instance.order.destination_country = order_data.pop('destination_country')
        instance.order.comment = order_data.pop('comment')
        instance.order.manager = order_data.pop('manager')
        instance.order.customer = order_data.pop('customer')
        instance.product_id = validated_data.pop('product_id')
        instance.sending_type = validated_data.pop('sending_type')
        instance.order.save()
        instance.save()
        return instance
