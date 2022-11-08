from django.urls import path

from apps.container_order.container_type.views import ContainerTypeOrderCreate, ContainerTypeOrderUpdate, \
    ContainerTypeOrderDelete

urlpatterns = [
    # CONTAINER_TYPE
    path('create/', ContainerTypeOrderCreate.as_view(), name='container_type_create'),
    path('update/<int:pk>/', ContainerTypeOrderUpdate.as_view(), name='container_type_update'),
    path('delete/<int:pk>/', ContainerTypeOrderDelete.as_view(), name='container_type_delete'),

]
