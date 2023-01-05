from django.urls import path

from apps.code.views import ApplicationCreate

urlpatterns = [
    path('application/create/', ApplicationCreate.as_view(), name='application_create')
]
