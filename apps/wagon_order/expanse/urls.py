from django.urls import path

from apps.wagon_order.expanse.views import WagonExpanseCreate

urlpatterns = [
    path('create/', WagonExpanseCreate.as_view(), name='expanse-create')
]
