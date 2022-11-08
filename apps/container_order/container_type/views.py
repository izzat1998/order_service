from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView

from apps.container_order.container_type.serializers import ContainerTypeOrderCreateSerializer, \
    ContainerTypeOrderUpdateSerializer
from apps.container_order.models import ContainerTypeOrder


class ContainerTypeOrderCreate(CreateAPIView):
    serializer_class = ContainerTypeOrderCreateSerializer
    queryset = ContainerTypeOrder.objects.all()


class ContainerTypeOrderUpdate(UpdateAPIView):
    lookup_field = 'pk'
    serializer_class = ContainerTypeOrderUpdateSerializer
    queryset = ContainerTypeOrder.objects.all()


class ContainerTypeOrderDelete(DestroyAPIView):
    lookup_field = 'pk'
    queryset = ContainerTypeOrder.objects.all()
