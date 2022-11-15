from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.container_order.models import ContainerOrder
from apps.container_order.serializers.container_order_create import ContainerOrderCreateSerializer
from apps.container_order.serializers.container_order_list import ContainerOrderListSerializer
from apps.container_order.serializers.container_order_update import ContainerOrderUpdateSerializer
from apps.container_order.serializers.serializers import ContainerOrderSerializer
from apps.order.models import Order


# Create your views here.
class ContainerOrderList(ListAPIView):
    search_fields = ['order__order_number', 'order__lot_number', 'order__shipper', 'order__consignee', 'order__date']
    filter_backends = [SearchFilter]
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
