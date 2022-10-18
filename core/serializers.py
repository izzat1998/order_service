from rest_framework import serializers

from core.models import Product, Station


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True)
    hc_code = serializers.IntegerField(required=True)
    etcng_code = serializers.IntegerField(required=True)
    etcng_name = serializers.CharField()

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name")
        instance.hc_code = validated_data.get("hc_code")
        instance.etcng_code = validated_data.get("etcng_code")
        instance.etcng_name = validated_data.get("etcng_name")
        instance.save()
        return instance


class StationSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True)
    code = serializers.CharField(required=True)
    railway_name = serializers.CharField(max_length=255, read_only=True)

    def create(self, validated_data):
        return Station.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name")
        instance.code = validated_data.get("code")
        instance.save()
        return instance
