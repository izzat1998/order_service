from django.db.models import Count, Sum, Case, When
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.container_order.models import ContainerOrder
from apps.order.models import Order, WagonOrder


# Create your views here.


class OrderStatistic(APIView):
    def get(self, request, *args, **kwargs):
        container_orders = ContainerOrder.objects.order_by('order__position').values('order__position').annotate(
            expanses=Sum('container_types__expanses__actual_costs__actual_cost'),
            agreed_rate=Sum('container_types__agreed_rate')
        ).all()

        wagon_orders = WagonOrder.objects.order_by('order__position').values('order__position').annotate(
            agreed_rate=(Sum('expanses__agreed_rate_per_tonn') * Sum('expanses__actual_weight')),
            expanse=Sum('expanses__actual_costs__actual_cost')

        ).all()
        statistic_data = {
            'container_orders': container_orders,
            'wagon_orders': wagon_orders
        }

        # statistic = {
        #     'rail_forwarder_count': Order.position_count(Order.POSITION_CHOICES[0][0]),
        #     'block_train_count': Order.position_count(Order.POSITION_CHOICES[1][0]),
        #     'multi_modal_count': Order.position_count(Order.POSITION_CHOICES[2][0])
        # }

        return Response(statistic_data)
