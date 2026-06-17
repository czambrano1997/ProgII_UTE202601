from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Crea o prepara el usuario administrador emily sin establecer una contraseña visible."

    def handle(self, *args, **options):
        User = get_user_model()
        usuario, creado = User.objects.get_or_create(username="emily")
        usuario.is_staff = True
        usuario.is_superuser = True
        usuario.is_active = True
        if creado:
            usuario.set_unusable_password()
        usuario.save()

        if creado:
            self.stdout.write(
                self.style.SUCCESS(
                    "Usuario emily creado sin contraseña utilizable. Ejecuta: python manage.py changepassword emily"
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    "Usuario emily preparado como administrador. No se modificó su contraseña existente."
                )
            )
