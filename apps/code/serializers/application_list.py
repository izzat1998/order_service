from rest_framework import serializers

from apps.code.models import Application
from apps.core.serializers import StationSerializer, ProductSerializer, TerritorySerializer
from apps.counterparty.serializers import CounterpartySerializer


class ApplicationListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    prefix = serializers.CharField(max_length=255)
    number = serializers.IntegerField(read_only=True)
    quantity = serializers.IntegerField(read_only=True)
    date = serializers.DateField(read_only=True)
    sending_type = serializers.ChoiceField(read_only=True, choices=Application.SENDING_TYPE)
    shipper = serializers.CharField(read_only=True)
    consignee = serializers.CharField(read_only=True)
    condition_of_carriage = serializers.CharField(read_only=True)
    agreed_rate = serializers.CharField(read_only=True)
    border_crossing = serializers.CharField(read_only=True)
    departure_country = serializers.CharField(read_only=True)
    destination_country = serializers.CharField(read_only=True)
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
