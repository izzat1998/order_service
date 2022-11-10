from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.container_order.expanse.serializers import ContainerExpanseCreateSerializer
from apps.container_order.models import ContainerExpanse, ContainerActualCost


class ContainerExpanseCreate(CreateAPIView):
    queryset = ContainerExpanse.objects.all()
    serializer_class = ContainerExpanseCreateSerializer


class ContainerExpanseUpdate(UpdateAPIView):
    queryset = ContainerExpanse.objects.all()
    serializer_class = ContainerExpanseCreateSerializer


class CounterpartyAddExpanse(APIView):
    def post(self, request, *args, **kwargs):
        preliminary_cost = request.POST.get('preliminary_cost')
        container_type_id = request.POST.get('container_type_id'),
        counterparty_id = request.POST.get('counterparty_id'),
        containers_expanse = ContainerExpanse.objects.filter(container_type=container_type_id)
        for container in containers_expanse:
            ContainerActualCost.objects.create(containers_expanse=container, preliminary_cost=preliminary_cost,
                                               counterparty_id=counterparty_id)
        return Response(status=201)