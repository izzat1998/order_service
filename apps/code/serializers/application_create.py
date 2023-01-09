from rest_framework import serializers

from apps.code.models import Application
from apps.code.utils import DocxService, ConvertToPdf
from apps.core.models import Territory
from apps.core.serializers import TerritorySerializer


class ApplicationCreateSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(default=1)
    prefix = serializers.CharField()
    date = serializers.DateField()
    period = serializers.CharField(allow_null=True, allow_blank=True)
    sending_type = serializers.ChoiceField(choices=Application.SENDING_TYPE)
    shipper = serializers.CharField(allow_null=True, allow_blank=True)
    consignee = serializers.CharField(allow_null=True, allow_blank=True)
    condition_of_carriage = serializers.CharField(allow_null=True, allow_blank=True)
    agreed_rate = serializers.CharField(allow_null=True, allow_blank=True)
    border_crossing = serializers.CharField(allow_null=True, allow_blank=True)
    departure_country = serializers.CharField(allow_null=True, allow_blank=True)
    destination_country = serializers.CharField(allow_null=True, allow_blank=True)
    rolling_stock_1 = serializers.CharField(allow_null=True, allow_blank=True)
    rolling_stock_2 = serializers.CharField(allow_null=True, allow_blank=True)
    paid_telegram = serializers.CharField(allow_null=True, allow_blank=True)
    departure_id = serializers.IntegerField()
    destination_id = serializers.IntegerField()
    containers_or_wagons = serializers.CharField(allow_null=True, allow_blank=True)
    product_id = serializers.IntegerField()
    loading_type = serializers.ChoiceField(
        choices=Application.LOADING_CHOICES
    )
    container_type = serializers.ChoiceField(choices=Application.CONTAINER_TYPE, allow_blank=True, allow_null=True)
    weight = serializers.CharField(max_length=50, allow_blank=True, allow_null=True, required=False)
    territories = TerritorySerializer(many=True)
    forwarder_id = serializers.IntegerField()
    manager = serializers.IntegerField()
    customer = serializers.IntegerField()

    def create(self, validated_data):
        territories = validated_data.pop('territories')
        application = Application.objects.create(**validated_data, number=Application.last_number() + 1)

        validated_data['number'] = str(application.number)
        validated_data['territories'] = territories
        docx_name, pdf_name = DocxService.create_doc_file(validated_data)
        path = ConvertToPdf.convert(docx_name, pdf_name)

        for territory in territories:
            application.territories.add(Territory.objects.filter(name=territory['name']).first())

        application.file = path
        application.save()

        return application
