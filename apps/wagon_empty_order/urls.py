from django.urls import path, include

from .views import (
    WagonEmptyOrderCreate,
    WagonEmptyOrderList,
    WagonEmptyOrderDetail, WagonEmptyOrderUpdate,
)

urlpatterns = [
    path("create/", WagonEmptyOrderCreate.as_view(), name="wagon_empty_order_create"),
    path("update/<int:order_number>/", WagonEmptyOrderUpdate.as_view(), name="wagon_empty_order_update"),
    path("list/", WagonEmptyOrderList.as_view(), name="wagon_empty_order_list"),
    path(
        "list/<int:order_number>/",
        WagonEmptyOrderDetail.as_view(),
        name="wagon_empty_order_list",
    ),
    path("expanse/", include("apps.wagon_empty_order.expanse.urls")),
]
