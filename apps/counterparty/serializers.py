from rest_framework import serializers

from apps.counterparty.models import CounterpartyCategory, Counterparty


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True)

    def create(self, validated_data):
        return CounterpartyCategory.objects.create(**validated_data)

    def validate(self, data):
        if CounterpartyCategory.objects.filter(name=data['name']).exists():
            raise serializers.ValidationError('Category with this name already exists')
        return data

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name")
        instance.save()
        return instance


class CounterpartySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True)

    def create(self, validated_data):
        return Counterparty.objects.create(**validated_data)

    def validate(self, data):
        if Counterparty.objects.filter(name=data['name']).exists():
            raise serializers.ValidationError('Category with this name already exists')
        return data

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name")
        instance.save()
        return instance
