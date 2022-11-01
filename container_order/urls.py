from django.urls import path

from container_order.counterparty_order.views import CounterPartyOrderList, CounterPartyOrderCreate, \
    CounterPartyOrderUpdate, CounterPartyOrderDelete
from container_order.preliminary_cost.views import ContainerPreliminaryCostCreate, ContainerPreliminaryCostUpdate, \
    ContainerPreliminaryCostDelete
from container_order.views import ContainerOrderList, ContainerOrderDetail, ContainerOrderUpdate, ContainerOrderDelete, \
    ContainerOrderCreate

urlpatterns = [
    path('list/', ContainerOrderList.as_view(), name='container_order_list'),
    path('list/<int:order_number>/', ContainerOrderDetail.as_view(), name='container_order_detail'),

    path('list/<int:order_number>/edit/', ContainerOrderUpdate.as_view(), name='container_order_update'),
    path('list/<int:order_number>/delete/', ContainerOrderDelete.as_view(), name='container_order_delete'),

    path('create/', ContainerOrderCreate.as_view(), name='container_order_create'),

    # COUNTERPARTY
    path('counterparty_list/', CounterPartyOrderList.as_view(), name='counterparty_list'),
    path('counterparty_create/', CounterPartyOrderCreate.as_view(), name='counterparty_create'),
    path('counterparty_update/<int:pk>/', CounterPartyOrderUpdate.as_view(), name='counterparty_create'),
    path('counterparty_delete/<int:pk>/', CounterPartyOrderDelete.as_view(), name='counterparty_delete'),

    # PRELIMINARY
    path('container_preliminary_cost_create/', ContainerPreliminaryCostCreate.as_view(),
         name='container_preliminary_cost_create'),
    path('container_preliminary_cost_update/<int:pk>/', ContainerPreliminaryCostUpdate.as_view(),
         name='container_preliminary_cost_update'),
    path('container_preliminary_cost_delete/<int:pk>/', ContainerPreliminaryCostDelete.as_view(),
         name='container_preliminary_cost_delete'),

]
