from rest_framework import serializers

from apps.container_order.models import ContainerActualCost, ContainerExpanse
from apps.core.models import Container


class ContainerActualCostSerializer(serializers.Serializer):
    counterparty_id = serializers.IntegerField()
    actual_cost = serializers.DecimalField(max_digits=10, decimal_places=2)


class ContainerExpanseCreateSerializer(serializers.Serializer):
    container = serializers.CharField(source='container.name')
    container_type_id = serializers.IntegerField()
    expanses = ContainerActualCostSerializer(many=True)

    def create(self, validated_data):
        container_name = validated_data.pop('container').pop('name')
        container, _ = Container.objects.get_or_create(name=container_name)
        expanse_container = ContainerExpanse.objects.create(container=container,
                                                            container_type_id=validated_data.pop('container_type_id'))

        for expanse in validated_data.pop('expanses'):
            ContainerActualCost.objects.create(
                counterparty_id=expanse.pop('counterparty_id'),
                actual_cost=expanse.pop('actual_cost'),
                container_expanse=expanse_container
            )
        return expanse_container
