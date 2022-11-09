from django.urls import path, include

urlpatterns = [
    path('counterparty/', include('apps.order.counterparty_order.urls')),
]
