
from rest_framework import serializers

from .models import (
    Curso,
    Inscripcion,
    Certificacion,
    SolicitudContacto
)


class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = "__all__"


class InscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscripcion
        fields = "__all__"


class CertificacionSerializer(serializers.ModelSerializer):
    curso_nombre = serializers.CharField(
        source="curso.nombre",
        read_only=True
    )

    class Meta:
        model = Certificacion
        fields = [
            "id",
            "alumno",
            "curso",
            "curso_nombre",
            "folio",
            "fecha_emision"
        ]


class SolicitudContactoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolicitudContacto
        fields = "__all__"
        read_only_fields = ("creado_en",)
