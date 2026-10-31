from django.db import models


class Curso(models.Model):
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    duracion_horas = models.PositiveIntegerField(default=20)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Inscripcion(models.Model):
    nombre = models.CharField(max_length=140)
    correo = models.EmailField()
    telefono = models.CharField(max_length=30)
    edad = models.PositiveIntegerField()

    # Campos corregidos (texto libre para curso y nivel)
    curso = models.CharField(max_length=120)          # Texto: "Inglés", "Computación", etc.
    nivel = models.CharField(max_length=120)          # Texto: "A2", "B1", etc.

    fecha_inicio = models.DateField()
    nuevo_ingreso = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True)

    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.curso} ({self.nivel})"


class Certificacion(models.Model):
    alumno = models.CharField(max_length=140)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="certificaciones")
    folio = models.CharField(max_length=50, unique=True)
    fecha_emision = models.DateField()

    def __str__(self):
        return f"{self.alumno} - {self.folio}"


class SolicitudContacto(models.Model):
    DESTINATARIOS = [
        ("yo", "Para mí"),
        ("hijo", "Para mi hijo/a"),
        ("otro", "Para otra persona"),
    ]

    MODALIDADES = [
        ("presencial", "Presencial"),
        ("online", "En línea"),
        ("ambas", "Cualquiera"),
    ]

    HORARIOS = [
        ("matutino", "Matutino"),
        ("vespertino", "Vespertino"),
        ("fines_semana", "Fines de semana"),
        ("flexible", "Flexible"),
    ]

    nombre = models.CharField(max_length=140)
    correo = models.EmailField()
    telefono = models.CharField(max_length=30)
    edad = models.PositiveIntegerField(null=True, blank=True)
    interes = models.CharField(max_length=150)
    dirigido_a = models.CharField(
        max_length=20,
        choices=DESTINATARIOS,
        default="yo"
    )
    modalidad = models.CharField(
        max_length=20,
        choices=MODALIDADES
    )
    horario = models.CharField(
        max_length=20,
        choices=HORARIOS
    )
    mensaje = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.interes}"

    class Meta:
        ordering = ["-creado_en"]
        verbose_name = "Solicitud de contacto"
        verbose_name_plural = "Solicitudes de contacto"
