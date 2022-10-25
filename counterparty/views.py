from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from core.utils import add_stations, add_products
from counterparty.models import CounterpartyCategory, Counterparty
from counterparty.serializers import CategorySerializer, CounterpartySerializer


# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']
    queryset = CounterpartyCategory.objects.all()

    def get_queryset(self):
        add_stations()
        add_products()


class CounterpartyViewSet(viewsets.ModelViewSet):
    filter_backends = [SearchFilter]
    search_fields = ['name']
    serializer_class = CounterpartySerializer
    queryset = Counterparty.objects.all()
