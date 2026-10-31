
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework.parsers import JSONParser
from django.conf import settings

from .models import Curso, Inscripcion, Certificacion, SolicitudContacto
from .serializers import (
    CursoSerializer,
    InscripcionSerializer,
    CertificacionSerializer,
    SolicitudContactoSerializer
)


class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all().order_by("nombre")
    serializer_class = CursoSerializer


class InscripcionViewSet(viewsets.ModelViewSet):
    queryset = Inscripcion.objects.all().order_by("-creado_en")
    serializer_class = InscripcionSerializer


class CertificacionViewSet(viewsets.ModelViewSet):
    queryset = Certificacion.objects.all().order_by("-fecha_emision")
    serializer_class = CertificacionSerializer


class ContactoAPIView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    def post(self, request):
        serializer = SolicitudContactoSerializer(data=request.data)

        if serializer.is_valid():
            solicitud = serializer.save()

            return Response(
                {
                    "mensaje": "Solicitud guardada correctamente.",
                    "id": solicitud.id
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
