from rest_framework.generics import CreateAPIView, UpdateAPIView

from apps.container_order.expanse.serializers import ContainerExpanseCreateSerializer
from apps.container_order.models import ContainerExpanse


class ContainerExpanseCreate(CreateAPIView):
    queryset = ContainerExpanse.objects.all()
    serializer_class = ContainerExpanseCreateSerializer


class ContainerExpanseUpdate(UpdateAPIView):
    queryset = ContainerExpanse.objects.all()
    serializer_class = ContainerExpanseCreateSerializer
