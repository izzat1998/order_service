from rest_framework import serializers
from ..models import ContainerTypeOrder, ContainerOrder


class ContainerTypeOrderCreateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    agreed_rate = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField(default=0)
    container_type = serializers.ChoiceField(
        choices=ContainerTypeOrder.CONTAINER_TYPE_CHOICES
    )
    order_number = serializers.IntegerField(source="order.order.order_number")

    def create(self, validated_data):
        container_order = ContainerOrder.objects.filter(
            order__order_number=validated_data.pop("order")
            .pop("order")
            .pop("order_number")
        ).first()
        return ContainerTypeOrder.objects.create(
            **validated_data, order=container_order
        )


class ContainerTypeOrderUpdateSerializer(serializers.Serializer):
    agreed_rate = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField(default=0)
    container_type = serializers.ChoiceField(
        choices=ContainerTypeOrder.CONTAINER_TYPE_CHOICES
    )
    order_number = serializers.IntegerField(read_only=True)

    def update(self, instance, validated_data):
        instance.quantity = validated_data.pop("quantity")
        instance.container_type = validated_data.pop("container_type")
        instance.agreed_rate = validated_data.pop("agreed_rate")
        instance.save()
        return instance
