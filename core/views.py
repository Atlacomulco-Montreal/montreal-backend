import logging
import os
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.conf import settings
from django.core.mail import send_mail

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.parsers import JSONParser

from .serializers import SolicitudContactoSerializer

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

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        # 1. Guardar primero en la base de datos
        solicitud = serializer.save()

        # 2. Preparar los datos del correo
        asunto = (
            f"Nueva solicitud de contacto - {solicitud.nombre}"
        )

        mensaje = f"""
NUEVA SOLICITUD DE INFORMACIÓN
MONTREAL ATLACOMULCO

Nombre: {solicitud.nombre}
Correo: {solicitud.correo}
Teléfono: {solicitud.telefono}

Interés: {solicitud.interes}
Dirigido a: {solicitud.get_dirigido_a_display()}
Modalidad: {solicitud.get_modalidad_display()}
Horario: {solicitud.get_horario_display()}
Edad: {solicitud.edad if solicitud.edad is not None else "No especificada"}

Mensaje:
{solicitud.mensaje}

Fecha de registro:
{solicitud.creado_en}
"""

        # 3. Enviar notificación a Montreal
        try:
            send_mail(
                subject=asunto,
                message=mensaje,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=False,
                reply_to=[solicitud.correo],
            )

            email_enviado = True

        except Exception:
            logging.exception(
                "No se pudo enviar el correo de la solicitud %s",
                solicitud.id
            )
            email_enviado = False

        # 4. Responder al frontend
        return Response(
            {
                "mensaje": (
                    "Solicitud guardada correctamente."
                    if email_enviado
                    else "Solicitud guardada, pero no se pudo enviar el correo."
                ),
                "id": solicitud.id,
                "email_enviado": email_enviado,
            },
            status=status.HTTP_201_CREATED
        )
