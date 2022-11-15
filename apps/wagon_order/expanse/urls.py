from django.urls import path

from apps.wagon_order.expanse.views import WagonExpanseCreate, WagonExpanseUpdate

urlpatterns = [
    path('create/', WagonExpanseCreate.as_view(), name='expanse-create'),
    path('update/<int:pk>/', WagonExpanseUpdate.as_view(), name='expanse-update')
]
