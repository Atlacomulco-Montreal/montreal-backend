
import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Crea un administrador usando variables de entorno temporales."

    def handle(self, *args, **options):
        User = get_user_model()

        username = os.environ.get("ADMIN_USERNAME")
        email = os.environ.get("ADMIN_EMAIL")
        password = os.environ.get("ADMIN_PASSWORD")

        if not username or not email or not password:
            raise CommandError(
                "Configura ADMIN_USERNAME, ADMIN_EMAIL y ADMIN_PASSWORD."
            )

        if User.objects.filter(username=username).exists():
            raise CommandError(
                "Ese usuario ya existe. No se realizaron cambios."
            )

        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Administrador {user.username} creado correctamente."
            )
        )
