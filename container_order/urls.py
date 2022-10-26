from django.urls import path

from container_order.views import ContainerOrderList, ContainerOrderDetail, ContainerOrderUpdate, ContainerOrderDelete, \
    ContainerOrderCreate, CounterPartyOrderCreate, CounterPartyOrderUpdate, CounterPartyOrderDelete, \
    CounterPartyOrderList

urlpatterns = [
    path('list/', ContainerOrderList.as_view(), name='container_order_list'),
    path('list/<int:order_number>/', ContainerOrderDetail.as_view(), name='container_order_detail'),

    path('list/<int:order_number>/edit/', ContainerOrderUpdate.as_view(), name='container_order_update'),
    path('list/<int:order_number>/delete/', ContainerOrderDelete.as_view(), name='container_order_delete'),

    path('create/', ContainerOrderCreate.as_view(), name='container_order_create'),


    path('counterparty_list/', CounterPartyOrderList.as_view(), name='counter_party_list'),
    path('counterparty_create/', CounterPartyOrderCreate.as_view(), name='counter_party_create'),
    path('counterparty_update/<int:pk>/', CounterPartyOrderUpdate.as_view(), name='counter_party_create'),
    path('counterparty_delete/<int:pk>/', CounterPartyOrderDelete.as_view(), name='counter_party_delete')

]
