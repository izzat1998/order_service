from django.urls import path

from apps.wagon_order.preliminary_cost.views import WagonPreliminaryCostCreate, WagonPreliminaryCostUpdate, \
    WagonPreliminaryCostDelete

urlpatterns = [
    path('create/', WagonPreliminaryCostCreate.as_view(), name='wagon_create_preliminary_cost'),
    path('update/<int:pk>/', WagonPreliminaryCostUpdate.as_view(), name='wagon_update_preliminary_cost'),
    path('delete/<int:pk>/', WagonPreliminaryCostDelete.as_view(), name='wagon_delete_preliminary_cost')
]
