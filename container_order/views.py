from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView, get_object_or_404, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from container_order.models import ContainerOrder, CounterPartyOrder
from container_order.serializers.container_order_create import ContainerOrderCreateSerializer
from container_order.serializers.container_order_list import ContainerOrderListSerializer
from container_order.serializers.container_order_update import ContainerOrderUpdateSerializer
from container_order.serializers.counterparty_order_serializer import \
    CounterPartyOrderCreateSerializer, CounterPartyUpdateSerializer, CounterPartyOrderListSerializer
from container_order.serializers.serializers import ContainerOrderSerializer
from order.models import Order


# Create your views here.
class ContainerOrderList(ListAPIView):
    serializer_class = ContainerOrderListSerializer
    queryset = ContainerOrder.objects.all().select_related('order__departure', 'order__destination',
                                                           'product')


class ContainerOrderDetail(APIView):
    def get(self, request, order_number):
        orders = ContainerOrder.objects.filter(order__order_number=order_number).select_related(
            'order__departure', 'order__destination',
            'product')

        serializer = ContainerOrderSerializer(orders, many=True)
        return Response(serializer.data)


class ContainerOrderCreate(APIView):
    def post(self, request):
        serializer = ContainerOrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response({"Order number": order.order_number}, status=status.HTTP_201_CREATED)


class ContainerOrderUpdate(APIView):
    def put(self, request, order_number):
        order = get_object_or_404(ContainerOrder, order__order_number=order_number)
        serializer = ContainerOrderUpdateSerializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response({"Order number": order.order.order_number}, status=status.HTTP_200_OK)


class ContainerOrderDelete(APIView):
    def delete(self, request, order_number):
        order = get_object_or_404(Order, order_number=order_number)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CounterPartyOrderList(ListAPIView):
    serializer_class = CounterPartyOrderListSerializer
    queryset = CounterPartyOrder.objects.all()


class CounterPartyOrderCreate(CreateAPIView):
    serializer_class = CounterPartyOrderCreateSerializer
    queryset = CounterPartyOrder.objects.all()


class CounterPartyOrderUpdate(UpdateAPIView):
    lookup_field = 'pk'
    serializer_class = CounterPartyUpdateSerializer
    queryset = CounterPartyOrder.objects.all()


class CounterPartyOrderDelete(DestroyAPIView):
    lookup_field = 'pk'
    queryset = CounterPartyOrder.objects.all()
