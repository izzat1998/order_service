from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from core.models import Product, Station
from core.serializers import ProductSerializer, StationSerializer
from core.utils import add_products


# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Return the given product.

    list:
    Return a list of all the existing products.

    create:
    Create a new product instance.

    update:
    Update an existing product instance.

    delete:
    Delete an existing product instance.
    """

    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'hc_code', 'etcng_code', 'etcng_name']
    queryset = Product.objects.all()


class StationViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Return the given station.

    list:
    Return a list of all the existing stations.

    create:
    Create a new station instance.

    update:
    Update an existing station instance.

    delete:
    Delete an existing station instance.
    """

    serializer_class = StationSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'code', 'railway_name']
    queryset = Station.objects.all()
