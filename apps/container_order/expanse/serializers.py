from rest_framework import serializers

from apps.container_order.models import ContainerActualCost, ContainerExpanse
from apps.core.models import Container


class ContainerActualCostSerializer(serializers.Serializer):
    counterparty_id = serializers.IntegerField()
    actual_cost = serializers.DecimalField(max_digits=10, decimal_places=2)


class ContainerExpanseCreateSerializer(serializers.Serializer):
    container_type_id = serializers.IntegerField()
    actual_costs = ContainerActualCostSerializer(many=True)

    def create(self, validated_data):
        validated_data.pop('quantity', None)
        expanse_container = ContainerExpanse.objects.create(container_type_id=validated_data.pop('container_type_id'))

        for expanse in validated_data.pop('actual_costs'):
            ContainerActualCost.objects.create(
                counterparty_id=expanse.pop('counterparty_id'),
                actual_cost=expanse.pop('actual_cost'),
                container_expanse=expanse_container
            )
        return expanse_container


class ContainerExpanseUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    container_name = serializers.CharField(source='container.name')

    def update(self, instance, validated_data):
        container, _ = Container.objects.get_or_create(name=validated_data.pop("container").pop("name"))
        instance.container = container
        instance.save()
        return instance
