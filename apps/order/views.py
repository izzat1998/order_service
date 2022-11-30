# Create your views here.
from rest_framework.generics import ListAPIView

from apps.order.models import Order
from apps.order.serializers.serializers import OrderSerializer


class OrderList(ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
