from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from getpass import getpass

class Command(BaseCommand):
    help = 'Actualiza la contraseña de un usuario'

    def handle(self, *args, **kwargs):
        # Solicitar el nombre de usuario
        username = input('Ingresa el nombre de usuario: ')

        # Intentar obtener el usuario
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'El usuario con nombre "{username}" no existe.'))
            return

        # Solicitar la nueva contraseña
        password = getpass('Ingresa la nueva contraseña: ')

        # Actualizar la contraseña del usuario
        user.set_password(password)
        user.save()

        self.stdout.write(self.style.SUCCESS(f'Contraseña para el usuario "{username}" actualizada exitosamente.'))
