# Create your views here.
from rest_framework.generics import ListAPIView

from .models import Order
from .serializers.serializers import OrderSerializer


class OrderList(ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all().select_related("departure", "destination")
