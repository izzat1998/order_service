from django.urls import path

from apps.code.views import ApplicationCreate, ApplicationDetail, ApplicationList, ApplicationUpdate

urlpatterns = [
    path('application/create/', ApplicationCreate.as_view(), name='application_create'),
    path('application/update/<int:id>/', ApplicationUpdate.as_view(), name='application_update'),
    path('application/list/', ApplicationList.as_view(), name='application_list'),
    path('application/list/<int:id>/', ApplicationDetail.as_view(), name='application_detail')
]
