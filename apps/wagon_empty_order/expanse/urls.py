from django.urls import path

from apps.wagon_empty_order.expanse.views import WagonEmptyExpanseUpdate, WagonEmptyActualCostUpdate

urlpatterns = [

    # path('update/<int:pk>/', WagonEmptyExpanseUpdate.as_view(), name='update-empty-wagon'),
    path('actual_cost/update/<int:pk>/', WagonEmptyActualCostUpdate.as_view(), name='update-empty-wagon')
]
