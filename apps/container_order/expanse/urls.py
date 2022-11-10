from django.urls import path

from apps.container_order.expanse.views import ContainerExpanseCreate, CounterpartyAddExpanse

urlpatterns = [
    path('create/', ContainerExpanseCreate.as_view(), name='container_expanse_create'),
    path('counterparty_add/', CounterpartyAddExpanse.as_view(), name='container_expanse_add')
]
