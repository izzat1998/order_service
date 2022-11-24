from django.db.models import Q
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from apps.container_order.models import CounterPartyOrder
from apps.container_order.serializers.container_order_create import CounterPartyOrderCreateSerializer
from apps.core.models import Station, Product

from apps.order.models import WagonOrder, Order
from apps.wagon_order.models import WagonPreliminaryCost, WagonExpanse, WagonActualCost


class PreliminaryCostCreateSerializer(serializers.Serializer):
    counterparty_id = serializers.IntegerField()
    category_id = serializers.IntegerField()
    preliminary_cost = serializers.DecimalField(max_digits=10, decimal_places=2)


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


class WagonOrderCreateSerializer(serializers.Serializer):
    order = OrderCreateSerializer()
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    weight = serializers.IntegerField()
    wagon_preliminary_costs = PreliminaryCostCreateSerializer(many=True)

    def validate(self, data):
        if WagonOrder.objects.filter(order__order_number=data['order']['order_number']).exists():
            raise serializers.ValidationError('Order number already exists')
        if not Station.objects.filter(Q(id=data['order']['departure_id']) or data['order']['destination_id']).exists():
            raise serializers.ValidationError('Departure or Destination station doesnt exist')
        if not Product.objects.filter(id=data['product_id']).exists():
            raise serializers.ValidationError('Product doesnt exist')
        return data

    def create(self, validated_data):
        wagon_preliminary_data = validated_data.pop('wagon_preliminary_costs')
        order_data = validated_data.pop('order')
        counterparty_data = order_data.pop('counterparties')
        wagon_order_data = validated_data
        quantity = validated_data.get('quantity')
        agreed_rate_per_tonn = validated_data.get('agreed_rate_per_tonn')
        counterparties = []

        def create_wagon_order(order_d, container_order_data):
            base_order = Order.objects.create(**order_d)
            order = WagonOrder.objects.create(order=base_order, **container_order_data)
            counterparty = CounterPartyOrderCreateSerializer(data=counterparty_data, many=True)
            if counterparty.is_valid(raise_exception=True):
                for counterparty in counterparty.data:
                    CounterPartyOrder.objects.create(**counterparty, order=base_order)
            return order, base_order

        def create_expanse(quantity, order):
            for i in range(quantity):
                wagon_expanse = WagonExpanse.objects.create(order=order, agreed_rate_per_tonn=agreed_rate_per_tonn)
                for counterparty in counterparties:
                    WagonActualCost.objects.create(actual_cost=counterparty['preliminary_cost'],
                                                   wagon_expanse=wagon_expanse,
                                                   counterparty_id=counterparty['counterparty'])

        def create_preliminary_cost(wagon_preliminary, parent_order, wagon_order):
            wagon_preliminary_cost = PreliminaryCostCreateSerializer(
                data=wagon_preliminary, many=True)
            if wagon_preliminary_cost.is_valid(raise_exception=True):
                for preliminary_cost in wagon_preliminary_cost.data:
                    counterparty = get_object_or_404(CounterPartyOrder, order=parent_order,
                                                     counterparty_id=preliminary_cost[
                                                         'counterparty_id'],
                                                     category_id=preliminary_cost['category_id']
                                                     )
                    WagonPreliminaryCost.objects.create(counterparty=counterparty,
                                                        preliminary_cost=preliminary_cost[
                                                            'preliminary_cost'],

                                                        order=wagon_order
                                                        )
                    counterparties.append({
                        'counterparty': counterparty.id,
                        'preliminary_cost': preliminary_cost['preliminary_cost']
                    })

        order, base_order = create_wagon_order(order_data, wagon_order_data)
        create_preliminary_cost(wagon_preliminary_data, base_order, order)
        create_expanse(quantity, order)
        return base_order
