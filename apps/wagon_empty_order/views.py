from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.order.models import WagonEmptyOrder
from apps.wagon_empty_order.serializers.serializers import WagonEmptyOrderSerializer
from apps.wagon_empty_order.serializers.wagon_empty_create import WagonEmptyOrderCreateSerializer
from apps.wagon_empty_order.serializers.wagon_empty_order_list import WagonEmptyOrderListSerializer


class WagonEmptyOrderCreate(APIView):
    def post(self, request):
        serializer = WagonEmptyOrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response({"Order number": order.order_number}, status=status.HTTP_201_CREATED)


class WagonEmptyOrderList(ListAPIView):
    serializer_class = WagonEmptyOrderListSerializer
    queryset = WagonEmptyOrder.objects.all().select_related('order__departure', 'order__destination')


class WagonEmptyOrderDetail(APIView):
    def get(self, request, order_number):
        orders = WagonEmptyOrder.objects.filter(order__order_number=order_number).select_related(
            'order__departure', 'order__destination')

        serializer = WagonEmptyOrderSerializer(orders, many=True)
        return Response(serializer.data)
