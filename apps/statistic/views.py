from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.order.models import Order


# Create your views here.


class OrderStatistic(APIView):
    def get(self, request, *args, **kwargs):
        statistic = {
            'rail_forwarder_count': Order.position_count(Order.POSITION_CHOICES[0][0]),
            'block_train_count': Order.position_count(Order.POSITION_CHOICES[1][0]),
            'multi_modal_count': Order.position_count(Order.POSITION_CHOICES[2][0])
        }

        return Response(statistic)
