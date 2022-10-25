from rest_framework import serializers

from container_order.models import ContainerExpanse
from core.models import Container


class ContainerOrderExpanseActualCost(serializers.Serializer):
    container_name = serializers.CharField()
    actual_cost = serializers.DecimalField(max_digits=10, decimal_places=2)


class ContainerOrderExpanseCreateSerializer(serializers.Serializer):
    counterparty_id = serializers.IntegerField()
    container_type_id = serializers.IntegerField()
    containers = ContainerOrderExpanseActualCost(many=True)

    def create(self, validated_data):
        counterparty_id = validated_data.pop('counterparty_id')
        container_type_id = validated_data.pop('container_type_id')
        result_create_data = []
        containers = validated_data.pop('containers', None)
        for container in containers:
            cntr, _ = Container.objects.get_or_create(name=container['container_name'])
            result_create_data.append(ContainerExpanse(
                counterparty_id=counterparty_id,
                container_id=cntr.id,
                actual_cost=container['actual_cost'],
                container_type_id=container_type_id
            ))
        containers = ContainerExpanse.objects.bulk_create(result_create_data)
        return containers
