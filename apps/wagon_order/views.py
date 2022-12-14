from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.order.models import WagonOrder, Order
from .serializers.serializers import WagonOrderSerializer
from .serializers.wagon_create import WagonOrderCreateSerializer
from .serializers.wagon_order_list import WagonOrderListSerializer
from .serializers.wagon_update import WagonOrderUpdateSerializer


# Create your views here.
class WagonOrderList(ListAPIView):
    serializer_class = WagonOrderListSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = WagonOrder.objects.filter(order__visible=True).select_related(
            "order__departure", "order__destination", "product"
        )
        manager = self.request.query_params.get('manager')
        if manager is not None:
            queryset = queryset.filter(order__manager=manager)
        return queryset


class WagonOrderDetail(APIView):
    def get(self, request, order_number):
        orders = (
            WagonOrder.objects.filter(order__order_number=order_number)
            .select_related("order__departure", "order__destination", "product")
            .prefetch_related(
                "order__counterparties__category",
                "order__counterparties__counterparty",
                "wagon_preliminary_costs__counterparty__counterparty",
                "wagon_preliminary_costs__counterparty__category",
                "expanses__actual_costs__counterparty__counterparty",
                "expanses__actual_costs__counterparty__category",
                "expanses__wagon",
            )
        )

        serializer = WagonOrderSerializer(orders, many=True)
        return Response(serializer.data)


class WagonOrderCreate(APIView):
    def post(self, request):
        serializer = WagonOrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(
            {"Order number": order.order_number}, status=status.HTTP_201_CREATED
        )


class WagonOrderUpdate(APIView):
    @extend_schema(request=None, responses=WagonOrderUpdateSerializer)
    def put(self, request, order_number):
        order = get_object_or_404(WagonOrder, order__order_number=order_number)
        serializer = WagonOrderUpdateSerializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(
            {"Order number": order.order.order_number}, status=status.HTTP_200_OK
        )


class WagonOrderDelete(APIView):
    def delete(self, request, order_number):
        order = get_object_or_404(Order, order_number=order_number)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
