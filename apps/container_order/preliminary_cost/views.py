from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView

from ..models import ContainerPreliminaryCost
from .serializers import (
    ContainerPreliminaryCreateSerializer,
    ContainerPreliminaryUpdateSerializer,
)


class ContainerPreliminaryCostCreate(CreateAPIView):
    serializer_class = ContainerPreliminaryCreateSerializer
    queryset = ContainerPreliminaryCost.objects.all()


class ContainerPreliminaryCostUpdate(UpdateAPIView):
    lookup_field = "pk"
    serializer_class = ContainerPreliminaryUpdateSerializer
    queryset = ContainerPreliminaryCost.objects.all()


class ContainerPreliminaryCostDelete(DestroyAPIView):
    lookup_field = "pk"
    queryset = ContainerPreliminaryCost.objects.all()
