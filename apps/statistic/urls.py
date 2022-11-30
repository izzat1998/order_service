from django.urls import path

from apps.statistic.views import OrderStatistic, OrderStatisticMonthly, OrderStatisticByUser

urlpatterns = [
    path('', OrderStatistic.as_view(), name='order_statistic'),
    path('monthly', OrderStatisticMonthly.as_view(), name='order_statistic_monthly'),
    path('users', OrderStatisticByUser.as_view(), name='user_statistic')
]
