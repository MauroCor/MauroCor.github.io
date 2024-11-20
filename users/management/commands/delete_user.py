from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Elimina un usuario por su nombre de usuario'

    def handle(self, *args, **kwargs):
        # Pedir al usuario que ingrese el nombre de usuario
        username = input('Ingresa el nombre de usuario que deseas buscar: ')

        # Buscar usuarios que contengan el nombre proporcionado
        users = User.objects.filter(username__icontains=username)
        
        if users.exists():
            self.stdout.write(self.style.SUCCESS(f'Coincidencias encontradas para "{username}":'))
            for user in users:
                # Mostrar detalles del usuario
                self.stdout.write(f'Username: {user.username} | Nombre: {user.first_name} {user.last_name} | Correo: {user.email}')
            
            # Confirmar si desea eliminar el usuario
            confirm = input(f'¿Quieres eliminar estos usuarios? (y/n): ')
            
            if confirm.lower() == 'y':
                # Eliminar usuarios
                for user in users:
                    user.delete()
                self.stdout.write(self.style.SUCCESS(f'Usuarios eliminados exitosamente.'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Operación cancelada.'))
        else:
            self.stdout.write(self.style.ERROR(f'No se encontraron usuarios que coincidan con "{username}".'))