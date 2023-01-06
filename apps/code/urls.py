from django.urls import path

from apps.code.views import ApplicationCreate, ApplicationDetail, ApplicationList

urlpatterns = [
    path('application/create/', ApplicationCreate.as_view(), name='application_create'),
    path('application/list/', ApplicationList.as_view(), name='application_list'),
    path('application/list/<int:id>/', ApplicationDetail.as_view(), name='application_detail')
]
