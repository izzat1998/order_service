from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from core.models import Product, Station
from core.serializers import ProductSerializer, StationSerializer
from core.utils import add_products


# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'hc_code', 'etcng_code', 'etcng_name']
    queryset = add_products()


class StationViewSet(viewsets.ModelViewSet):
    serializer_class = StationSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'code', 'railway_name']
    queryset = Station.objects.all()
