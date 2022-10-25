from django.db.models import Q
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from container_order.models import ContainerTypeOrder, ContainerOrder, CounterPartyOrder, ContainerPreliminaryCost
from core.models import Station, Product
from order.models import Order


class ContainerPreliminaryCostUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    preliminary_cost = serializers.DecimalField(decimal_places=2, max_digits=10)


class CounterPartyOrderUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    category_id = serializers.IntegerField()
    counterparty_id = serializers.IntegerField()


class ContainerTypeOrderUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    agreed_rate = serializers.DecimalField(decimal_places=2, max_digits=10)
    quantity = serializers.IntegerField()
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
    counterparties = CounterPartyOrderUpdateSerializer(many=True)


class ContainerOrderUpdateSerializer(serializers.Serializer):
    order = OrderUpdateSerializer()
    container_types = ContainerTypeOrderUpdateSerializer(many=True)
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
        counterparty_data = order_data.pop('counterparties')
        container_type_data = validated_data.pop('container_types')

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
        instance.order.save()

        counterparty = CounterPartyOrderUpdateSerializer(data=counterparty_data, many=True)
        if counterparty.is_valid(raise_exception=True):
            for counterparty_data in counterparty.data:
                counterparty = get_object_or_404(CounterPartyOrder, id=counterparty_data['id'])
                counterparty.counterparty_id = counterparty_data['counterparty_id']
                counterparty.category_id = counterparty_data['category_id']
                counterparty.save()
        container_type = ContainerTypeOrderUpdateSerializer(data=container_type_data, many=True)

        if container_type.is_valid(raise_exception=True):
            for container_type in container_type.data:
                container_preliminary_cost_data = container_type.pop('container_preliminary_costs')

                container_type_order = get_object_or_404(ContainerTypeOrder, id=container_type['id'])
                container_type_order.agreed_rate = container_type['agreed_rate']
                container_type_order.quantity = container_type['quantity']
                container_type_order.container_type = container_type['container_type']
                container_type_order.save()
                container_preliminary_cost = ContainerPreliminaryCostUpdateSerializer(
                    data=container_preliminary_cost_data, many=True)
                if container_preliminary_cost.is_valid(raise_exception=True):
                    for preliminary_cost in container_preliminary_cost.data:
                        preliminary = get_object_or_404(ContainerPreliminaryCost, id=preliminary_cost['id'])
                        preliminary.preliminary_cost = preliminary_cost['preliminary_cost']
                        preliminary.save()

        return instance
