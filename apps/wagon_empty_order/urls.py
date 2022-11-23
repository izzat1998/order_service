from django.urls import path

from apps.wagon_empty_order.views import WagonEmptyOrderCreate, WagonEmptyOrderList, WagonEmptyOrderDetail

urlpatterns = [
    path('create/', WagonEmptyOrderCreate.as_view(), name='wagon_empty_order_create'),
    path('list/', WagonEmptyOrderList.as_view(), name='wagon_empty_order_list'),
    path('list/<int:order_number>/', WagonEmptyOrderDetail.as_view(), name='wagon_empty_order_list'),

]
