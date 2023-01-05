from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ProductViewSet, StationViewSet, TerritoryViewSet

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")
router.register(r"stations", StationViewSet, basename="station")
router.register(r"territories", TerritoryViewSet, basename="territory")

urlpatterns = [
    path("", include(router.urls)),
]
