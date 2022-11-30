from django.db.models import Count, Sum, Case, When, F
from django.db.models.functions import TruncMonth, ExtractMonth, ExtractYear
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.container_order.models import ContainerOrder, ContainerExpanse
from apps.order.models import WagonOrder, Order


# Create your views here.

class OrderStatistic(APIView):
    def get(self, request, *args, **kwargs):
        container_orders = ContainerOrder.objects.order_by('order__position').values('order__position').annotate(
            agreed_rate=Sum('container_types__expanses__agreed_rate'),
            containers_count=Count('id')
        )
        wagon_orders = WagonOrder.objects.order_by('order__position').values('order__position').annotate(
            agreed_rate=Sum(F('expanses__agreed_rate_per_tonn') * F('expanses__actual_weight'),
                            wagons_count=Count('id'))
        )

        container = {
            'type': "ContainerOrder",
            'stat': container_orders
        }
        wagon = {
            'type': "WagonOrder",
            'stat': wagon_orders
        }

        # statistic = {
        #     'rail_forwarder_count': Order.position_count(Order.POSITION_CHOICES[0][0]),
        #     'block_train_count': Order.position_count(Order.POSITION_CHOICES[1][0]),
        #     'multi_modal_count': Order.position_count(Order.POSITION_CHOICES[2][0])
        # }

        return Response([container, wagon])


class OrderStatisticMonthly(APIView):
    def get(self, request, *args, **kwargs):
        monthly_orders = Order.objects.annotate(month=ExtractMonth('date'),
                                                year=ExtractYear('date')).values('month', 'year').annotate(
            total=Count('*')).values('month', 'year', 'total')

        container_expanses = ContainerExpanse.objects.annotate(month=ExtractMonth('container_type__order__order__date'),
                                                               year=ExtractYear(
                                                                   'container_type__order__order__date')).values(
            'month',
            'year').annotate(
            total_agreed_rate=Sum('agreed_rate')).values('month', 'year', 'total_agreed_rate')

        return Response({'monthly_orders': monthly_orders,
                         'monthly_agreed_rate': container_expanses
                         }
                        )


class OrderStatisticByUser(APIView):
    def get(self, request):
        orders = Order.objects.order_by('manager').values('manager').annotate(count=Count('id'))
        return Response({'user_orders': orders})
