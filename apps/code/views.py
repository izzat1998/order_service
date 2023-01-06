from pyexpat import model

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView

from rest_framework.response import Response
from rest_framework.views import APIView

from apps.code.models import Application
from apps.code.serializers.application_create import ApplicationCreateSerializer
from apps.code.serializers.application_list import ApplicationListSerializer
from apps.code.serializers.serializers import ApplicationSerializer


class ApplicationCreate(APIView):
    @extend_schema(request=None, responses=ApplicationCreateSerializer)
    def post(self, request):
        serializer = ApplicationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        application = serializer.save()
        return Response(
            {"Application number": application.number}, status=status.HTTP_201_CREATED
        )


class ApplicationList(ListAPIView):
    queryset = Application.objects.all().select_related('departure', 'destination', 'product',
                                                        'forwarder').prefetch_related('territories')
    serializer_class = ApplicationListSerializer


class ApplicationDetail(RetrieveAPIView):
    lookup_field = 'id'
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
