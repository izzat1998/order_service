from django.urls import path

from apps.container_order.preliminary_cost.views import ContainerPreliminaryCostCreate, ContainerPreliminaryCostUpdate, \
    ContainerPreliminaryCostDelete

urlpatterns = [
    path('create/', ContainerPreliminaryCostCreate.as_view(),
         name='container_preliminary_cost_create'),
    path('update/<int:pk>/', ContainerPreliminaryCostUpdate.as_view(),
         name='container_preliminary_cost_update'),
    path('delete/<int:pk>/', ContainerPreliminaryCostDelete.as_view(),
         name='container_preliminary_cost_delete'),
]
