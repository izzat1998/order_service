from django.urls import path

from apps.container_order.expanse.views import ContainerExpanseCreate

urlpatterns = [
    path('create/', ContainerExpanseCreate.as_view(), name='container_expanse_create')
]
