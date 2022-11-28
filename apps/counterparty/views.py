from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from apps.counterparty.models import CounterpartyCategory, Counterparty
from apps.counterparty.serializers import CategorySerializer, CounterpartySerializer


# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']
    queryset = CounterpartyCategory.objects.all()


class CounterpartyViewSet(viewsets.ModelViewSet):
    filter_backends = [SearchFilter]
    search_fields = ['name']
    serializer_class = CounterpartySerializer
    queryset = Counterparty.objects.all()
