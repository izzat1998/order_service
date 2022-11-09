from rest_framework import serializers


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    hc_code = serializers.IntegerField(read_only=True)
    etcng_code = serializers.IntegerField(read_only=True)


class StationSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100, read_only=True)
    code = serializers.CharField(max_length=100, read_only=True)
    railway_name = serializers.CharField(max_length=255, read_only=True)
