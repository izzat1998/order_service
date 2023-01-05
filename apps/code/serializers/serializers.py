from rest_framework import serializers

from apps.code.models import Application
from apps.core.serializers import StationSerializer, ProductSerializer, TerritorySerializer
from apps.counterparty.serializers import CounterpartySerializer


class ApplicationSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    prefix = serializers.CharField(max_length=255)
    number = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1)
    date = serializers.DateField()
    sending_type = serializers.CharField(choices=Application.SENDING_TYPE)
    shipper = serializers.CharField(allow_null=True, allow_blank=True)
    consignee = serializers.CharField(allow_null=True, allow_blank=True)
    condition_of_carriage = serializers.CharField(allow_null=True, allow_blank=True)
    agreed_rate = serializers.CharField(allow_null=True, allow_blank=True)
    border_crossing = serializers.CharField(allow_null=True, allow_blank=True)
    departure_country = serializers.CharField(allow_null=True, allow_blank=True)
    destination_country = serializers.CharField(allow_null=True, allow_blank=True)
    departure = StationSerializer()
    destination = StationSerializer()
    product = ProductSerializer()
    loading_type = serializers.ChoiceField(
        choices=Application.LOADING_CHOICES,
    )
    container_type = serializers.ChoiceField(choices=Application.CONTAINER_TYPE)
    weight = serializers.CharField(max_length=50, allow_blank=True, allow_null=True)
    territories = TerritorySerializer()
    forwarder = CounterpartySerializer()
    manager = serializers.IntegerField()
    customer = serializers.IntegerField()
