from django.urls import path

from order.views import ContainerOrderList, ContainerOrderDetail, ContainerOrderCreate

urlpatterns = [
    path('list/', ContainerOrderList.as_view(), name='container_order_list'),
    path('list/<int:order_number>/', ContainerOrderDetail.as_view(), name='container_order_detail'),
    path('create/', ContainerOrderCreate.as_view(), name='container_order_create'),
    path('create2/', ContainerOrderCreate.as_view(), name='container_order_create2'),
]
