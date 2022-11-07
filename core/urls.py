from django.urls import include, path
from rest_framework.routers import DefaultRouter

from core.views import ProductViewSet, StationViewSet


router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'stations', StationViewSet, basename='station')

urlpatterns = [

    path('', include(router.urls)),
]
