from django.urls import path

from apps.wagon_order.expanse.views import WagonExpanseCreate, WagonExpanseUpdate, WagonActualCostUpdate, \
    WagonExpanseWagonAll

urlpatterns = [
    path('create/', WagonExpanseCreate.as_view(), name='expanse-create'),
    path('update/<int:pk>/', WagonExpanseUpdate.as_view(), name='expanse-update'),
    path('wagon_add/', WagonExpanseWagonAll.as_view(), name='wagon-expanse-all'),
    path('actual_cost/update/<int:pk>/', WagonActualCostUpdate.as_view(), name='actual-cost-update')
]
