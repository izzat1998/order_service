from rest_framework import serializers

from apps.code.models import Application
from apps.core.models import Territory
from apps.core.serializers import TerritorySerializer


class ApplicationCreateSerializer(serializers.Serializer):
    prefix = serializers.CharField(max_length=255)
    number = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1)
    date = serializers.DateField()
    sending_type = serializers.ChoiceField(choices=Application.SENDING_TYPE)
    shipper = serializers.CharField(allow_null=True, allow_blank=True)
    consignee = serializers.CharField(allow_null=True, allow_blank=True)
    condition_of_carriage = serializers.CharField(allow_null=True, allow_blank=True)
    agreed_rate = serializers.CharField(allow_null=True, allow_blank=True)
    border_crossing = serializers.CharField(allow_null=True, allow_blank=True)
    departure_country = serializers.CharField(allow_null=True, allow_blank=True)
    destination_country = serializers.CharField(allow_null=True, allow_blank=True)
    departure_id = serializers.IntegerField()
    destination_id = serializers.IntegerField()
    product_id = serializers.IntegerField()
    loading_type = serializers.ChoiceField(
        choices=Application.LOADING_CHOICES,
    )
    container_type = serializers.ChoiceField(choices=Application.CONTAINER_TYPE)
    weight = serializers.CharField(max_length=50, allow_blank=True, allow_null=True)
    territories = TerritorySerializer(many=True)
    forwarder_id = serializers.IntegerField()
    manager = serializers.IntegerField()
    customer = serializers.IntegerField()

    def create(self, validated_data):
        territories = validated_data.pop('territories')
        application = Application.objects.create(**validated_data)
        for territory in territories:
            application.territories.add(Territory.objects.filter(name=territory['name']).first())
        application.number = Application.last_number() + 1
        application.save()

        return application
