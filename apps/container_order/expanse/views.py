from rest_framework import serializers

from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.container_order.expanse.serializers import ContainerExpanseCreateSerializer, \
    ContainerActualCostUpdateSerializer
from apps.container_order.models import ContainerExpanse, ContainerActualCost
from apps.container_order.serializers.serializers import ContainerExpanseSerializer
from apps.core.models import Container


class ContainerExpanseCreate(CreateAPIView):
    queryset = ContainerExpanse.objects.all()
    serializer_class = ContainerExpanseCreateSerializer


class ContainerExpanseUpdateAll(APIView):
    def put(self, request):
        container_type_id = request.data['container_type_id']
        counterparty_id = request.data['counterparty_id']
        actual_cost = request.data['actual_cost']
        actual_costs = ContainerActualCost.objects.filter(counterparty_id=counterparty_id,
                                                          container_expanse__container_type_id=container_type_id)
        for ac in actual_costs:
            ac.actual_cost = actual_cost
            ac.save()
        return Response(status=200)


class ContainerExpanseContainerAll(APIView):
    def put(self, request):
        container_type_id = request.data['container_type_id']
        new_containers = request.data['containers']
        old_containers = ContainerExpanse.objects.filter(container_type_id=container_type_id).order_by('-id')
        for new_c, old_c in zip(new_containers, old_containers):
            container, _ = Container.objects.get_or_create(name=new_c)
            old_c.container = container
        ContainerExpanse.objects.bulk_update(old_containers, ['container'])
        return Response(status=200)


class ContainerExpanseUpdate(APIView):
    def put(self, request, pk):
        container_type_id = request.data['container_type_id']
        container_expanse = ContainerExpanse.objects.filter(pk=pk).first()
        if request.data['container_name'] == '':
            container_expanse.container = None
            container_expanse.save()
            serializer = ContainerExpanseSerializer(container_expanse)
            return Response({"container": serializer.data.get('container')})
        else:
            if ContainerExpanse.objects.filter(container_type_id=container_type_id,
                                               container__name=request.data['container_name']).exists():
                raise serializers.ValidationError({'error': 'Container is already exists'})

            container, _ = Container.objects.get_or_create(name=request.data['container_name'])
            container_expanse.container = container
            container_expanse.save()
            serializer = ContainerExpanseSerializer(container_expanse)
            return Response({"container": serializer.data.get('container')})


class ContainerExpanseDelete(DestroyAPIView):
    lookup_field = 'pk'
    queryset = ContainerExpanse.objects.all()


class ContainerActualCostUpdate(UpdateAPIView):
    lookup_field = 'pk'
    queryset = ContainerActualCost.objects.all()
    serializer_class = ContainerActualCostUpdateSerializer


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
