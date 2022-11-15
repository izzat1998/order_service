from rest_framework.generics import CreateAPIView, UpdateAPIView

from apps.wagon_order.expanse.serializers import WagonExpanseCreateSerializer
from apps.wagon_order.models import WagonExpanse


class WagonExpanseCreate(CreateAPIView):
    serializer_class = WagonExpanseCreateSerializer
    queryset = WagonExpanse.objects.all()


class WagonExpanseUpdate(UpdateAPIView):
    queryset = WagonExpanse.objects.all()
    serializer_class = WagonExpanseCreateSerializer