from django.urls import path

from apps.wagon_empty_order.expanse.views import WagonEmptyExpanseUpdate

urlpatterns = [

    path('update/<int:pk>/', WagonEmptyExpanseUpdate.as_view(), name='update-empty-wagon')
]
