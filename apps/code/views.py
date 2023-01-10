from pyexpat import model

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView

from apps.code.models import Application
from apps.code.serializers.application_create_update import ApplicationCreateUpdateSerializer
from apps.code.serializers.application_list import ApplicationListSerializer
from apps.code.serializers.serializers import ApplicationSerializer


class ApplicationCreate(APIView):
    @extend_schema(request=None, responses=ApplicationCreateUpdateSerializer)
    def post(self, request):
        serializer = ApplicationCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        application = serializer.save()
        return Response(
            {"application_number": application.number,
             "application_file": application.file.url
             }, status=status.HTTP_201_CREATED
        )


class ApplicationUpdate(APIView):
    @extend_schema(request=None, responses=ApplicationCreateUpdateSerializer)
    def put(self, request, id):
        application = get_object_or_404(Application, id=id)
        serializer = ApplicationCreateUpdateSerializer(application, data=request.data)
        serializer.is_valid(raise_exception=True)
        application = serializer.save()
        return Response(
            {"application_number": application.number,
             "application_file": application.file.url
             }, status=status.HTTP_200_OK
        )


class ApplicationList(ListAPIView):
    queryset = Application.objects.all().select_related('departure', 'destination', 'product',
                                                        'forwarder').prefetch_related('territories')
    serializer_class = ApplicationListSerializer


class ApplicationDetail(RetrieveAPIView):
    lookup_field = 'id'
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
