from rest_framework import serializers

from apps.container_order.models import ContainerExpanse


# class WagonExpanseCreateSerializer(serializers.Serializer):
#     container_type_id = serializers.IntegerField()
#     actual_costs = ContainerActualCostSerializer(many=True)
#     actual_weight = serializers.DecimalField(max_digits=)
#     def create(self, validated_data):
#         validated_data.pop('quantity', None)
#         expanse_container = ContainerExpanse.objects.create(container_type_id=validated_data.pop('container_type_id'))
#
#         for expanse in validated_data.pop('actual_costs'):
#             ContainerActualCost.objects.create(
#                 counterparty_id=expanse.pop('counterparty_id'),
#                 actual_cost=expanse.pop('actual_cost'),
#                 container_expanse=expanse_container
#             )
#         return expanse_container
