from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Muestra la lista de usuarios'

    def handle(self, *args, **kwargs):
        # Obtener todos los usuarios
        users = User.objects.all()

        # Verificar si hay usuarios
        if users.exists():
            self.stdout.write(self.style.SUCCESS('Lista de usuarios:'))
            for user in users:
                self.stdout.write(f'Usuario: {user.username}, Nombre: {user.get_full_name()}, Correo: {user.email}')
        else:
            self.stdout.write(self.style.WARNING('No hay usuarios registrados.'))
