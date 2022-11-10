from django.urls import path, include

from apps.wagon_order.views import WagonOrderList, WagonOrderDetail, WagonOrderCreate, WagonOrderUpdate, \
    WagonOrderDelete

urlpatterns = [
    path('list/', WagonOrderList.as_view(), name='wagon_order_list'),
    path('list/<int:order_number>/', WagonOrderDetail.as_view(), name='wagon_order_detail'),
    path('create/', WagonOrderCreate.as_view(), name='wagon_order_create'),
    path('update/<int:order_number>/', WagonOrderUpdate.as_view(), name='wagon_order_update'),
    path('delete/<int:order_number>/', WagonOrderDelete.as_view(), name='wagon_order_create'),
    path('preliminary_cost/', include('apps.wagon_order.preliminary_cost.urls')),
]
