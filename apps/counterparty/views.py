from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from .models import CounterpartyCategory, Counterparty
from .serializers import CategorySerializer, CounterpartySerializer


# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    filter_backends = [SearchFilter]
    search_fields = ["name"]

    queryset = CounterpartyCategory.objects.all()


class CounterpartyViewSet(viewsets.ModelViewSet):
    filter_backends = [SearchFilter, DjangoFilterBackend, ]
    search_fields = ["name"]
    filterset_fields = ['is_used_for_code', ]
    serializer_class = CounterpartySerializer
    queryset = Counterparty.objects.all()
