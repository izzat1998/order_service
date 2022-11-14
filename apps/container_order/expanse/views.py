from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.container_order.expanse.serializers import ContainerExpanseCreateSerializer, ContainerExpanseUpdateSerializer
from apps.container_order.models import ContainerExpanse, ContainerActualCost


class ContainerExpanseCreate(CreateAPIView):
    queryset = ContainerExpanse.objects.all()
    serializer_class = ContainerExpanseCreateSerializer


class ContainerExpanseUpdate(UpdateAPIView):
    queryset = ContainerExpanse.objects.all()
    serializer_class = ContainerExpanseUpdateSerializer


class ContainerExpanseDelete(DestroyAPIView):
    lookup_field = 'pk'
    queryset = ContainerExpanse.objects.all()


class CounterpartyAddExpanse(APIView):
    def post(self, request, *args, **kwargs):
        preliminary_cost = request.data['preliminary_cost']
        container_type_id = request.data['container_type_id']
        counterparty_id = request.data['counterparty_id']
        containers_expanse = ContainerExpanse.objects.filter(container_type_id=container_type_id)
        for container in containers_expanse:
            ContainerActualCost.objects.create(container_expanse=container, actual_cost=preliminary_cost,
                                               counterparty_id=counterparty_id)
        return Response(status=201)
