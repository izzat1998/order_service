from django.urls import path, include

from apps.order.views import OrderList

urlpatterns = [
    path('counterparty/', include('apps.order.counterparty_order.urls')),
    path('list/', OrderList.as_view(), name='order-list'),
]
