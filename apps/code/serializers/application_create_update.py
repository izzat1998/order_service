import os

from rest_framework import serializers

from apps.code.models import Application
from apps.code.utils import DocxService, ConvertToPdf
from apps.core.models import Territory
from apps.core.serializers import TerritorySerializer


class ApplicationCreateUpdateSerializer(serializers.Serializer):
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

    def update(self, instance, validated_data):
        old_path = instance.file.path
        instance.quantity = validated_data.get('quantity')
        instance.prefix = validated_data.get('prefix')
        instance.date = validated_data.get('date')
        instance.period = validated_data.get('period')
        instance.sending_type = validated_data.get('sending_type')
        instance.shipper = validated_data.get('shipper')
        instance.consignee = validated_data.get('consignee')
        instance.condition_of_carriage = validated_data.get('condition_of_carriage')
        instance.agreed_rate = validated_data.get('agreed_rate')
        instance.border_crossing = validated_data.get('border_crossing')
        instance.departure_country = validated_data.get('departure_country')
        instance.destination_country = validated_data.get('destination_country')
        instance.rolling_stock_1 = validated_data.get('rolling_stock_1')
        instance.rolling_stock_2 = validated_data.get('rolling_stock_2')
        instance.paid_telegram = validated_data.get('paid_telegram')
        instance.departure_id = validated_data.get('departure_id')
        instance.destination_id = validated_data.get('destination_id')
        instance.containers_or_wagons = validated_data.get('containers_or_wagons')
        instance.product_id = validated_data.get('product_id')
        instance.loading_type = validated_data.get('loading_type')
        instance.container_type = validated_data.get('container_type')
        instance.weight = validated_data.get('weight')
        instance.forwarder_id = validated_data.get('forwarder_id')
        instance.manager = validated_data.get('manager')
        instance.customer = validated_data.get('customer')
        territories = validated_data.get('territories')
        instance.territories.clear()
        for territory in territories:
            instance.territories.add(Territory.objects.filter(name=territory['name']).first())
        instance.save()

        try:
            validated_data['number'] = instance.number
            docx_name, pdf_name = DocxService.create_doc_file(validated_data)
            path = ConvertToPdf.convert(docx_name, pdf_name)
            instance.file = path
        except Exception:
            raise serializers.ValidationError('Error while creating file')

        os.remove(old_path)
        instance.save()
        return instance
