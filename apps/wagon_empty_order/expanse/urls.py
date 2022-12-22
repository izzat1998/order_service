from django.urls import path

from .views import (
    WagonEmptyExpanseUpdate,
    WagonEmptyActualCostUpdate, WagonEmptyExpanseWagonAll, WagonExpanseUpdateWagonAll, WagonEmptyCounterPartyAddExpanse
)

urlpatterns = [
    path(
        "actual_cost/update/<int:pk>/",
        WagonEmptyActualCostUpdate.as_view(),
        name="update-empty-wagon",
    ),
    path(
        "update/<int:pk>/", WagonEmptyExpanseUpdate.as_view(), name="update_empty_wagon"
    ),
    path("wagon_add/", WagonEmptyExpanseWagonAll.as_view(), name="wagon_empty_expanse_all"),
    path("actual_cost_to_all/", WagonExpanseUpdateWagonAll.as_view(), name="wagon_empty_actual_cost_all"),
    path(
        "counterparty_add/",
        WagonEmptyCounterPartyAddExpanse.as_view(),
        name="wagon_counterparty_add",
    ),
]
