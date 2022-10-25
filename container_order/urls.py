from django.urls import path

from container_order.views import ContainerOrderList, ContainerOrderDetail, ContainerOrderUpdate, ContainerOrderDelete, \
    ContainerOrderExpanseCreate, ContainerOrderCreate

urlpatterns = [
    path('list/', ContainerOrderList.as_view(), name='container_order_list'),
    path('list/<int:order_number>/', ContainerOrderDetail.as_view(), name='container_order_detail'),

    path('list/<int:order_number>/edit/', ContainerOrderUpdate.as_view(), name='container_order_update'),
    path('list/<int:order_number>/delete/', ContainerOrderDelete.as_view(), name='container_order_delete'),

    path('list/<int:order_number>/expanse/create/', ContainerOrderExpanseCreate.as_view(),
         name='container_order_expanse_create'),
    path('create/', ContainerOrderCreate.as_view(), name='container_order_create'),

]
