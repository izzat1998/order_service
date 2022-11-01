from rest_framework import serializers

from container_order.models import CounterPartyOrder, ContainerOrder


class CounterPartyOrderListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    order_number = serializers.IntegerField(source='order.order_number')
    category = serializers.CharField(source='category.name')
    counterparty = serializers.CharField(source='counterparty.name')


class CounterPartyOrderCreateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    order_number = serializers.IntegerField(source='order.order_number')
    category_id = serializers.IntegerField()
    counterparty_id = serializers.IntegerField()

    def validate(self, data):
        if CounterPartyOrder.objects.filter(order__order_number=data['order']['order_number'],
                                            category_id=data['category_id'],
                                            counterparty_id=data['counterparty_id']).exists():
            raise serializers.ValidationError('Order with this category and counterparty already exists')
        return data

    def create(self, validated_data):
        order_number = validated_data.pop('order').pop('order_number')
        container_order = ContainerOrder.objects.filter(order__order_number=order_number).first()
        counterparty = CounterPartyOrder.objects.create(**validated_data, order=container_order.order)
        return counterparty


class CounterPartyUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    order_id = serializers.IntegerField(read_only=True)
    category_id = serializers.IntegerField()
    counterparty_id = serializers.IntegerField()

    def update(self, instance, validated_data):
        instance.category_id = validated_data.get('category_id')
        instance.counterparty_id = validated_data.get('counterparty_id')
        instance.save()
        return instance
