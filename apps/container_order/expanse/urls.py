from django.urls import path

from apps.container_order.expanse.views import ContainerExpanseCreate, CounterpartyAddExpanse, ContainerExpanseUpdate, \
    ContainerExpanseDelete, ContainerActualCostUpdate, ContainerExpanseUpdateAll, ContainerExpanseContainerAll

urlpatterns = [
    path('create/', ContainerExpanseCreate.as_view(), name='container_expanse_create'),
    path('update/<int:pk>/', ContainerExpanseUpdate.as_view(), name='container_expanse_update'),
    path('delete/<int:pk>/', ContainerExpanseDelete.as_view(), name='container_expanse_delete'),
    path('counterparty_add/', CounterpartyAddExpanse.as_view(), name='container_expanse_add'),

    path('actual_cost/update/<int:pk>/', ContainerActualCostUpdate.as_view(),
         name='container_expanse_actual_cost_update'),

    # Custom
    path('actual_cost_to_all/', ContainerExpanseUpdateAll.as_view(), name='container_expanse_actual_cost_all'),
    path('container_to_all/', ContainerExpanseContainerAll.as_view(), name='container_to_all')
]
