from django.urls import path

from apps.statistic.views import OrderStatistic

urlpatterns = [
    path('', OrderStatistic.as_view(), name='order_statistic')
]
