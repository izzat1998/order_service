from rest_framework import serializers

from container_order.models import CounterPartyOrder


class CounterPartyOrderListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    order_number = serializers.CharField(source='order.order_number')
    category = serializers.CharField(source='category.name')
    counterparty = serializers.CharField(source='counterparty.name')


class CounterPartyOrderCreateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    order_id = serializers.IntegerField()
    category_id = serializers.IntegerField()
    counterparty_id = serializers.IntegerField()

    def validate(self, data):
        if CounterPartyOrder.objects.filter(order_id=data['order_id'], category_id=data['category_id'],
                                            counterparty_id=data['counterparty_id']).exists():
            raise serializers.ValidationError('Order with this category and counterparty already exists')

    def create(self, validated_data):
        counterparty = CounterPartyOrder.objects.create(**validated_data)
        return counterparty


class CounterPartyUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    order_id = serializers.IntegerField(read_only=True)
    category_id = serializers.IntegerField()
    counterparty_id = serializers.IntegerField()

    def update(self, instance, validated_data):
        instance.category_id = validated_data.get('category_id')
        instance.counterparty_id = validated_data.get('counterparty_id')
        return instance
