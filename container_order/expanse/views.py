from rest_framework.generics import CreateAPIView, UpdateAPIView

from container_order.expanse.serializers import ContainerExpanseCreateSerializer
from container_order.models import ContainerExpanse


class ContainerExpanseCreate(CreateAPIView):
    queryset = ContainerExpanse.objects.all()
    serializer_class = ContainerExpanseCreateSerializer


class ContainerExpanseUpdate(UpdateAPIView):
    queryset = ContainerExpanse.objects.all()
    serializer_class = ContainerExpanseCreateSerializer
