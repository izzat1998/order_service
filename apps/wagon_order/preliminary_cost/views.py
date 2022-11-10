from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView

from apps.wagon_order.models import WagonPreliminaryCost
from apps.wagon_order.preliminary_cost.serializers import WagonPreliminaryCostUpdateSerializer, \
    WagonPreliminaryCostCreateSerializer


class WagonPreliminaryCostCreate(CreateAPIView):
    serializer_class = WagonPreliminaryCostCreateSerializer
    queryset = WagonPreliminaryCost.objects.all()


class WagonPreliminaryCostUpdate(UpdateAPIView):
    lookup_field = 'pk'
    serializer_class = WagonPreliminaryCostUpdateSerializer
    queryset = WagonPreliminaryCost.objects.all()


class WagonPreliminaryCostDelete(DestroyAPIView):
    lookup_field = 'pk'
    queryset = WagonPreliminaryCost.objects.all()
