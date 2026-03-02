from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from cards.models import Vehicle


class Command(BaseCommand):
    help = 'Create user groups with permissions'

    def handle(self, *args, **options):
        # Get content type for Vehicle model
        vehicle_ct = ContentType.objects.get_for_model(Vehicle)

        # Get existing permissions
        add_vehicle = Permission.objects.get(codename='add_vehicle', content_type=vehicle_ct)
        change_vehicle = Permission.objects.get(codename='change_vehicle', content_type=vehicle_ct)
        delete_vehicle = Permission.objects.get(codename='delete_vehicle', content_type=vehicle_ct)
        view_vehicle = Permission.objects.get(codename='view_vehicle', content_type=vehicle_ct)

        # Create or get groups
        # 1. Admin - all permissions
        admin_group, created = Group.objects.get_or_create(name='Администратор')
        admin_group.permissions.set([add_vehicle, change_vehicle, delete_vehicle, view_vehicle])
        status = 'Created' if created else 'Exists'
        self.stdout.write(f"[OK] {status}: Администратор (Admin) group")

        # 2. Supervisor - edit and delete
        supervisor_group, created = Group.objects.get_or_create(name='Руководитель')
        supervisor_group.permissions.set([change_vehicle, delete_vehicle, view_vehicle])
        status = 'Created' if created else 'Exists'
        self.stdout.write(f"[OK] {status}: Руководитель (Supervisor) group")

        # 3. Specialist - add and edit
        specialist_group, created = Group.objects.get_or_create(name='Специалист')
        specialist_group.permissions.set([add_vehicle, change_vehicle, view_vehicle])
        status = 'Created' if created else 'Exists'
        self.stdout.write(f"[OK] {status}: Специалист (Specialist) group")

        # 4. User - view only
        user_group, created = Group.objects.get_or_create(name='Пользователь')
        user_group.permissions.set([view_vehicle])
        status = 'Created' if created else 'Exists'
        self.stdout.write(f"[OK] {status}: Пользователь (User) group")

        self.stdout.write(self.style.SUCCESS('\nAll groups initialized successfully!'))
