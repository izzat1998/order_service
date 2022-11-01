from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView

from container_order.models import ContainerPreliminaryCost, CounterPartyOrder
from container_order.preliminary_cost.serializers import CounterPreliminaryCreateSerializer, \
    CounterPreliminaryUpdateSerializer


class ContainerPreliminaryCostCreate(CreateAPIView):
    serializer_class = CounterPreliminaryCreateSerializer
    queryset = ContainerPreliminaryCost.objects.all()


class ContainerPreliminaryCostUpdate(UpdateAPIView):
    lookup_field = 'pk'
    serializer_class = CounterPreliminaryUpdateSerializer
    queryset = ContainerPreliminaryCost.objects.all()


class ContainerPreliminaryCostDelete(DestroyAPIView):
    lookup_field = 'pk'
    queryset = CounterPartyOrder.objects.all()
