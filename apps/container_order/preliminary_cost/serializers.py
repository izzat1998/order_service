from rest_framework import serializers

from ..models import ContainerPreliminaryCost


class ContainerPreliminaryCreateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    preliminary_cost = serializers.DecimalField(max_digits=10, decimal_places=2)
    counterparty_id = serializers.IntegerField()
    container_type_id = serializers.IntegerField()

    def create(self, validated_data):
        return ContainerPreliminaryCost.objects.create(**validated_data)


class ContainerPreliminaryUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    preliminary_cost = serializers.DecimalField(max_digits=10, decimal_places=2)
    counterparty_id = serializers.IntegerField(read_only=True)
    container_type_id = serializers.IntegerField(read_only=True)

    def update(self, instance, validated_data):
        instance.preliminary_cost = validated_data.get("preliminary_cost")
        instance.save()
        return instance
