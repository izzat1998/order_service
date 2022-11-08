from rest_framework import serializers


class ContainerOrderExpanseActualCost(serializers.Serializer):
    container_name = serializers.CharField()
    actual_cost = serializers.DecimalField(max_digits=10, decimal_places=2)
