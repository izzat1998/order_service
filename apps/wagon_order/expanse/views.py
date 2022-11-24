from rest_framework import serializers
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.models import Wagon
from apps.wagon_order.expanse.serializers import WagonExpanseCreateSerializer
from apps.wagon_order.models import WagonExpanse
from apps.wagon_order.serializers.serializers import WagonExpanseSerializer


class WagonExpanseCreate(CreateAPIView):
    serializer_class = WagonExpanseCreateSerializer
    queryset = WagonExpanse.objects.all()


class WagonExpanseUpdate(APIView):
    def put(self, request, pk):
        wagon_expanse = WagonExpanse.objects.filter(pk=pk).select_related('wagon').first()
        if 'wagon_name' in request.data and request.data['wagon_name'] == '':
            wagon_expanse.wagon = None
            wagon_expanse.save()
            serializer = WagonExpanseSerializer(wagon_expanse)
            return Response(serializer.data)
        elif 'wagon_name' in request.data:
            wagon, _ = Wagon.objects.get_or_create(name=request.data['wagon_name'])
            wagon_expanse.wagon = wagon
        if 'agreed_rate_per_tonn' in request.data:
            wagon_expanse.agreed_rate_per_tonn = request.data['agreed_rate_per_tonn']
        if 'actual_weight' in request.data:
            wagon_expanse.actual_weight = request.data['actual_weight']
        wagon_expanse.save()
        data = {
            'wagon_name': wagon_expanse.wagon.name,
            'agreed_rate_per_tonn': wagon_expanse.agreed_rate_per_tonn,
            'actual_weight': wagon_expanse.actual_weight,
        }
        return Response(data)
