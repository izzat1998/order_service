from django.contrib.admin.utils import lookup_field
from django.views.generic import UpdateView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.models import Wagon
from apps.wagon_empty_order.expanse.serializers import WagonEmptyActualCostUpdateSerializer
from apps.wagon_empty_order.models import WagonEmptyExpanse, WagonEmptyActualCost
from apps.wagon_empty_order.serializers.serializers import WagonEmptyActualCostSerializer


class WagonEmptyExpanseUpdate(APIView):
    def put(self, request, pk):
        wagon_empty_expanse = WagonEmptyExpanse.objects.filter(pk=pk).first()
        if 'wagon_name' in request.data and request.data['wagon_name'] == '':
            wagon_empty_expanse.wagon = None
            wagon_empty_expanse.save()
            return Response({"wagon_name": wagon_empty_expanse.wagon})
        elif 'wagon_name' in request.data:
            if WagonEmptyExpanse.objects.filter(wagon__name=request.data['wagon_name']).exists():
                raise serializers.ValidationError({'error': 'Wagon is already exists'})

            wagon, _ = Wagon.objects.get_or_create(name=request.data['wagon_name'])
            wagon_empty_expanse.wagon = wagon
            wagon_empty_expanse.save()
        if 'agreed_rate' in request.data:
            wagon_empty_expanse.agreed_rate = request.data['agreed_rate']
            wagon_empty_expanse.save()
        data = {
            'wagon_name': wagon_empty_expanse.wagon.name if wagon_empty_expanse.wagon else '',
            'agreed_rate': wagon_empty_expanse.agreed_rate,
        }
        return Response(data)


class WagonEmptyActualCostUpdate(UpdateView):
    lookup_field = 'pk'
    model = WagonEmptyActualCost
    serializer_class = WagonEmptyActualCostUpdateSerializer
