from rest_framework import serializers
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.models import Wagon
from .serializers import (
    WagonExpanseCreateSerializer,
    WagonActualCostUpdateSerializer,
)
from ..models import WagonExpanse, WagonActualCost
from ...container_order.models import CounterPartyOrder
from ...order.models import Order


class WagonExpanseCreate(CreateAPIView):
    serializer_class = WagonExpanseCreateSerializer
    queryset = WagonExpanse.objects.all()


class WagonExpanseWagonAll(APIView):
    def put(self, request):
        order_number = request.data["order_number"]
        new_wagons = request.data["wagon"]
        old_wagons = WagonExpanse.objects.filter(
            order__order__order_number=order_number
        ).order_by("-id")
        for new_w, old_w in zip(new_wagons, old_wagons):
            wagon, _ = Wagon.objects.get_or_create(name=new_w)
            old_w.wagon = wagon
        WagonExpanse.objects.bulk_update(old_wagons, ["wagon"])
        return Response(status=200)


class WagonExpanseUpdateWagonAll(APIView):
    def put(self, request):
        order_number = request.data["order_number"]
        counterparty_id = request.data["counterparty_id"]
        actual_cost = request.data["actual_cost"]
        actual_costs = WagonActualCost.objects.filter(
            counterparty_id=counterparty_id,
            wagon_expanse__order__order__order_number=order_number,
        )
        for ac in actual_costs:
            ac.actual_cost = actual_cost
            ac.save()
        return Response(status=200)


class WagonExpanseUpdate(APIView):
    def put(self, request, pk):
        wagon_expanse = (
            WagonExpanse.objects.filter(pk=pk).select_related("wagon").first()
        )
        if "wagon_name" in request.data and request.data["wagon_name"] == "":
            wagon_expanse.wagon = None

        elif "wagon_name" in request.data:
            if WagonExpanse.objects.filter(
                    wagon__name=request.data["wagon_name"]
            ).exists():
                raise serializers.ValidationError({"error": "Wagon is already exists"})
            wagon, _ = Wagon.objects.get_or_create(name=request.data["wagon_name"])
            wagon_expanse.wagon = wagon
        if "agreed_rate_per_tonn" in request.data:
            wagon_expanse.agreed_rate_per_tonn = request.data["agreed_rate_per_tonn"]
        if "actual_weight" in request.data:
            wagon_expanse.actual_weight = request.data["actual_weight"]
        wagon_expanse.save()

        data = {
            "wagon_name": wagon_expanse.wagon.name if wagon_expanse.wagon else "",
            "agreed_rate_per_tonn": wagon_expanse.agreed_rate_per_tonn,
            "actual_weight": wagon_expanse.actual_weight,
        }
        return Response(data)


class WagonActualCostUpdate(UpdateAPIView):
    lookup_field = "pk"
    queryset = WagonActualCost.objects.all()
    serializer_class = WagonActualCostUpdateSerializer


class WagonCounterPartyAddExpanse(APIView):
    def post(self, request):
        preliminary_cost = request.data["preliminary_costs"]
        counterparty_id = request.data["counterparty_id"]
        category_id = request.data["category_id"]
        order_number = request.data["order_number"]
        order = Order.objects.filter(order_number=order_number).first()
        counterparty_order_id = CounterPartyOrder.objects.create(order=order, category_id=category_id,
                                                                 counterparty_id=counterparty_id).id
        wagon_expanse = WagonExpanse.objects.filter(order__order_number=order_number)

        for wagon in wagon_expanse:
            WagonActualCost.objects.create(
                wagon_expanse=wagon,
                actual_cost=preliminary_cost,
                counterparty_id=counterparty_order_id,
            )
        return Response(status=201)
