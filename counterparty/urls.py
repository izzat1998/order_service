from django.urls import include, path
from rest_framework.routers import DefaultRouter

from counterparty.views import CategoryViewSet, CounterpartyViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'counterparties', CounterpartyViewSet, basename='counterpartiescounterparty')

urlpatterns = [
    path('', include(router.urls)),
]
