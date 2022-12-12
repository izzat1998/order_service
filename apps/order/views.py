# Create your views here.

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Order
from .serializers.serializers import OrderSerializer


class OrderList(APIView):
    def get(self, request):
        orders = Order.objects.all()
        if 'manager' in request.GET:
            orders = orders.filter(manager=request.GET['manager'])
        if 'order_number' in request.GET:
            orders = orders.filter(order_number=request.GET['order_number'])
        if 'position' in request.GET:
            orders = orders.filter(position=request.GET['position'])
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
