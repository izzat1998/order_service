from drf_spectacular.utils import extend_schema
from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView

from apps.code.serializers.application_create import ApplicationCreateSerializer


class ApplicationCreate(APIView):
    @extend_schema(request=None, responses=ApplicationCreateSerializer)
    def post(self, request):
        serializer = ApplicationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        application = serializer.save()
        return Response(
            {"Application number": application.number}, status=status.HTTP_201_CREATED
        )
