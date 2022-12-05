from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)

from apps.container_order.models import CounterPartyOrder
from .serializers import (
    CounterPartyOrderListSerializer,
    CounterPartyOrderCreateSerializer,
    CounterPartyUpdateSerializer,
)


class CounterPartyOrderList(ListAPIView):
    serializer_class = CounterPartyOrderListSerializer
    queryset = CounterPartyOrder.objects.all().select_related(
        "order", "counterparty", "category"
    )


class CounterPartyOrderCreate(CreateAPIView):
    serializer_class = CounterPartyOrderCreateSerializer
    queryset = CounterPartyOrder.objects.all().select_related(
        "order", "counterparty", "category"
    )


class CounterPartyOrderUpdate(UpdateAPIView):
    lookup_field = "pk"
    serializer_class = CounterPartyUpdateSerializer
    queryset = CounterPartyOrder.objects.all().select_related(
        "order", "counterparty", "category"
    )


class CounterPartyOrderDelete(DestroyAPIView):
    lookup_field = "pk"
    queryset = CounterPartyOrder.objects.all().select_related(
        "order", "counterparty", "category"
    )
