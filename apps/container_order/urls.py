from django.urls import path, include

from apps.container_order.views import ContainerOrderList, ContainerOrderDetail, ContainerOrderUpdate, \
    ContainerOrderDelete, \
    ContainerOrderCreate

urlpatterns = [
    path('list/', ContainerOrderList.as_view(), name='container_order_list'),
    path('list/<int:order_number>/', ContainerOrderDetail.as_view(), name='container_order_detail'),
    path('list/<int:order_number>/edit/', ContainerOrderUpdate.as_view(), name='container_order_update'),
    path('list/<int:order_number>/delete/', ContainerOrderDelete.as_view(), name='container_order_delete'),

    path('create/', ContainerOrderCreate.as_view(), name='container_order_create'),
    path('preliminary_cost/', include('apps.container_order.preliminary_cost.urls')),
    path('container_type/', include('apps.container_order.container_type.urls')),
    path('expanse/', include('apps.container_order.expanse.urls'))
]
