from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from getpass import getpass

class Command(BaseCommand):
    help = 'Crea un usuario normal con nombre y apellido'

    def handle(self, *args, **kwargs):
        # Solicitar el nombre de usuario
        username = input('Ingresa el nombre de usuario: ')
        
        # Solicitar el nombre completo
        first_name = input('Ingresa el nombre: ')
        last_name = input('Ingresa el apellido: ')
        
        # Solicitar la contraseña
        password = getpass('Ingresa la contraseña: ')
        
        # Crear el usuario con los datos proporcionados
        User.objects.create_user(
            username=username,
            email='test@a.com', 
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        self.stdout.write(self.style.SUCCESS(f'Usuario {username} creado exitosamente con nombre {first_name} {last_name}.'))
