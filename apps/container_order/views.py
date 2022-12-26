from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ContainerOrder
from .serializers.container_order_create import (
    ContainerOrderCreateSerializer,
)
from .serializers.container_order_list import (
    ContainerOrderListSerializer,
)
from .serializers.container_order_update import (
    ContainerOrderUpdateSerializer,
)
from .serializers.serializers import ContainerOrderSerializer
from apps.order.models import Order


# Create your views here.
class ContainerOrderList(ListAPIView):
    search_fields = [
        "order__order_number",
        "order__lot_number",
        "order__shipper",
        "order__consignee",
        "order__date",
    ]
    filter_backends = [SearchFilter]
    serializer_class = ContainerOrderListSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = ContainerOrder.container_order_objects.get_list()
        manager = self.request.query_params.get('manager')
        if manager is not None:
            queryset = queryset.filter(order__manager=manager)
        return queryset


class ContainerOrderDetail(APIView):
    def get(self, request, order_number):
        orders = ContainerOrder.container_order_objects.get_by_order_number(
            order_number=order_number
        )
        serializer = ContainerOrderSerializer(orders, many=True)
        return Response(serializer.data)


class ContainerOrderCreate(APIView):
    def post(self, request):
        serializer = ContainerOrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(
            {"Order number": order.order_number}, status=status.HTTP_201_CREATED
        )


class ContainerOrderUpdate(APIView):
    def put(self, request, order_number):
        order = get_object_or_404(ContainerOrder, order__order_number=order_number)
        serializer = ContainerOrderUpdateSerializer(
            order, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(
            {"Order number": order.order.order_number}, status=status.HTTP_200_OK
        )


class ContainerOrderDelete(APIView):
    def delete(self, request, order_number):
        order = get_object_or_404(Order, order_number=order_number)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
