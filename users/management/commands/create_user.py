from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from getpass import getpass

class Command(BaseCommand):
    help = 'Crea un usuario normal'

    def handle(self, *args, **kwargs):
        username = input('Ingresa user: ')
        password = getpass('Ingresa password: ')
        
        User.objects.create_user(username=username, email='test@a.com', password=password)
        
        self.stdout.write(self.style.SUCCESS(f'Usuario {username} creado exitosamente'))
