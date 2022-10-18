from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from counterparty.models import Category, Counterparty
from counterparty.serializers import CategorySerializer, CounterpartySerializer


# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']
    queryset = Category.objects.all()


class CounterpartyViewSet(viewsets.ModelViewSet):
    filter_backends = [SearchFilter]
    search_fields = ['name']
    serializer_class = CounterpartySerializer
    queryset = Counterparty.objects.all()
