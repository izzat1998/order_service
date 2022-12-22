from django.contrib.admin.utils import lookup_field

from rest_framework import serializers
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.models import Wagon
from .serializers import (
    WagonEmptyActualCostUpdateSerializer,
)
from ..models import WagonEmptyExpanse, WagonEmptyActualCost
from ...container_order.models import CounterPartyOrder
from ...order.models import Order
from ...wagon_order.models import WagonExpanse


class WagonEmptyExpanseUpdate(APIView):
    def put(self, request, pk):
        wagon_empty_expanse = WagonEmptyExpanse.objects.filter(pk=pk).first()
        if "wagon_name" in request.data and request.data["wagon_name"] == "":
            wagon_empty_expanse.wagon = None
            wagon_empty_expanse.save()
            return Response({"wagon_name": wagon_empty_expanse.wagon})
        elif "wagon_name" in request.data:
            if WagonEmptyExpanse.objects.filter(
                    wagon__name=request.data["wagon_name"]
            ).exists():
                raise serializers.ValidationError({"error": "Wagon is already exists"})

            wagon, _ = Wagon.objects.get_or_create(name=request.data["wagon_name"])
            wagon_empty_expanse.wagon = wagon
            wagon_empty_expanse.save()
        if "agreed_rate" in request.data:
            wagon_empty_expanse.agreed_rate = request.data["agreed_rate"]
            wagon_empty_expanse.save()
        data = {
            "wagon_name": wagon_empty_expanse.wagon.name
            if wagon_empty_expanse.wagon
            else "",
            "agreed_rate": wagon_empty_expanse.agreed_rate,
        }
        return Response(data)


class WagonEmptyCounterPartyAddExpanse(APIView):
    def post(self, request):
        preliminary_cost = request.data["preliminary_cost"]
        counterparty_id = request.data["counterparty_id"]
        category_id = request.data["category_id"]
        order_number = request.data["order_number"]
        order = Order.objects.filter(order_number=order_number).first()
        counterparty_order_id = CounterPartyOrder.objects.create(order=order, category_id=category_id,
                                                                 counterparty_id=counterparty_id).id
        wagon_expanse = WagonEmptyExpanse.objects.filter(order__order__order_number=order_number)

        for wagon in wagon_expanse:
            WagonEmptyActualCost.objects.create(
                wagon_expanse=wagon,
                actual_cost=preliminary_cost,
                counterparty_id=counterparty_order_id,
            )
        return Response(status=201)


class WagonExpanseUpdateWagonAll(APIView):
    def put(self, request):
        order_number = request.data["order_number"]
        counterparty_id = request.data["counterparty_id"]
        actual_cost = request.data["actual_cost"]
        actual_costs = WagonEmptyActualCost.objects.filter(
            counterparty_id=counterparty_id,
            wagon_expanse__order__order__order_number=order_number,
        )
        if len(actual_costs) == 0:
            return Response({'error': "Not Found"}, status=404)
        for ac in actual_costs:
            ac.actual_cost = actual_cost
            ac.save()

        return Response(status=200)


class WagonEmptyExpanseWagonAll(APIView):
    def put(self, request):
        order_number = request.data["order_number"]
        new_wagons = request.data["wagon"]
        old_wagons = WagonEmptyExpanse.objects.filter(
            order__order__order_number=order_number
        ).order_by("-id")
        for new_w, old_w in zip(new_wagons, old_wagons):
            wagon, _ = Wagon.objects.get_or_create(name=new_w)
            old_w.wagon = wagon
        WagonEmptyExpanse.objects.bulk_update(old_wagons, ["wagon"])
        return Response(status=200)


class WagonEmptyActualCostUpdate(UpdateAPIView):
    lookup_field = "pk"
    queryset = WagonEmptyActualCost.objects.all()
    serializer_class = WagonEmptyActualCostUpdateSerializer
