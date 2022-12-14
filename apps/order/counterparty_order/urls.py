# COUNTERPARTY
from django.urls import path

from .views import (
    CounterPartyOrderList,
    CounterPartyOrderCreate,
    CounterPartyOrderUpdate,
    CounterPartyOrderDelete,
)

urlpatterns = [
    # CONTAINER_TYPE
    path("list/", CounterPartyOrderList.as_view(), name="counterparty_list"),
    path("create/", CounterPartyOrderCreate.as_view(), name="counterparty_create"),
    path(
        "update/<int:pk>/",
        CounterPartyOrderUpdate.as_view(),
        name="counterparty_create",
    ),
    path(
        "delete/<int:pk>/",
        CounterPartyOrderDelete.as_view(),
        name="counterparty_delete",
    ),
]
