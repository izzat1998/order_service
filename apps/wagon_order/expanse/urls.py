from django.urls import path

from .views import (
    WagonExpanseCreate,
    WagonExpanseUpdate,
    WagonActualCostUpdate,
    WagonExpanseWagonAll, WagonExpanseUpdateWagonAll,
    WagonCounterPartyAddExpanse
)

urlpatterns = [
    path("create/", WagonExpanseCreate.as_view(), name="expanse_create"),
    path("update/<int:pk>/", WagonExpanseUpdate.as_view(), name="expanse_update"),
    path("wagon_add/", WagonExpanseWagonAll.as_view(), name="wagon_expanse_all"),
    path("actual_cost_to_all/", WagonExpanseUpdateWagonAll.as_view(), name="wagon_actual_cost_all"),
    path(
        "actual_cost/update/<int:pk>/",
        WagonActualCostUpdate.as_view(),
        name="actual-cost-update",
    ),
    path(
        "counterparty_add/",
        WagonCounterPartyAddExpanse.as_view(),
        name="wagon_counterparty_add",
    )
]
