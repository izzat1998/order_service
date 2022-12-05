from django.urls import path

from .views import (
    WagonEmptyExpanseUpdate,
    WagonEmptyActualCostUpdate,
)

urlpatterns = [
    path(
        "actual_cost/update/<int:pk>/",
        WagonEmptyActualCostUpdate.as_view(),
        name="update-empty-wagon",
    ),
    path(
        "update/<int:pk>/", WagonEmptyExpanseUpdate.as_view(), name="update-empty-wagon"
    ),
]
