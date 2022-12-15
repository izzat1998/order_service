# Create your views here.

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Order
from .serializers.serializers import OrderSerializer
from ..core.models import Container


class OrderList(APIView):
    def get(self, request):

        orders = Order.objects.filter(visible=True)
        if 'container' in request.GET:
            orders = orders.filter(container_order__container_types__expanses__container__name__icontains=request.GET[
                'container']).distinct('order_number')
        if 'manager' in request.GET:
            orders = orders.filter(manager=request.GET['manager'])
        if 'order_number' in request.GET:
            orders = orders.filter(order_number=request.GET['order_number'])
        if 'position' in request.GET:
            orders = orders.filter(position=request.GET['position'])
        for order in orders:
            if hasattr(order, 'wagon_order'):
                order.child_type = 'wagon_order'
            elif hasattr(order, 'container_order'):
                order.child_type = 'container_order'
            else:
                order.child_type = 'wagon_empty_order'
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
