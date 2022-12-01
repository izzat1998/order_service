from rest_framework import serializers


class WagonEmptyActualCostUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    actual_cost = serializers.DecimalField(max_digits=10, decimal_places=2)

    def update(self, instance, validata_data):
        instance.actual_cost = validata_data["actual_cost"]
        instance.save()
        return instance
