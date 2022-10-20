from django.urls import path

from order.views import ContainerOrderList, ContainerOrderDetail, ContainerOrderCreate, ContainerOrderUpdate

urlpatterns = [
    path('list/', ContainerOrderList.as_view(), name='container_order_list'),
    path('list/<int:order_number>/', ContainerOrderDetail.as_view(), name='container_order_detail'),
    path('list/<int:order_number>/edit/', ContainerOrderUpdate.as_view(), name='container_order_update'),
    path('create/', ContainerOrderCreate.as_view(), name='container_order_create'),

]
