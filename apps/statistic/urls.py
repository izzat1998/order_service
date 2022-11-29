from django.urls import path

from apps.statistic.views import OrderStatistic, OrderStatisticMonthly

urlpatterns = [
    path('', OrderStatistic.as_view(), name='order_statistic'),
    path('/monthly', OrderStatisticMonthly.as_view(), name='order_statistic_monthly')
]
