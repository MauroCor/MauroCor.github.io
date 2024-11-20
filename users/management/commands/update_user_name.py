from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Actualiza el nombre y apellido de un usuario'

    def handle(self, *args, **kwargs):
        # Solicitar el nombre de usuario
        username = input('Ingresa el nombre de usuario: ')
        
        try:
            # Obtener el usuario por el nombre de usuario
            user = User.objects.get(username=username)
            
            # Solicitar los nuevos nombre y apellido
            first_name = input('Ingresa el nuevo nombre: ')
            last_name = input('Ingresa el nuevo apellido: ')
            
            # Actualizar los campos
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            
            self.stdout.write(self.style.SUCCESS(f'Usuario {username} actualizado exitosamente'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'El usuario {username} no existe'))
