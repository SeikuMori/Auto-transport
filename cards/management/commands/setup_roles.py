"""
Management command to set up role-based access control (RBAC) system.

Creates 4 groups with appropriate permissions for the Vehicle Fleet Management System:
1. Администратор (Admin) - Full access to all models
2. Руководитель (Manager) - Can view and edit vehicles, maintenance schedules
3. Специалист (Specialist) - Can view vehicles and maintenance, add new records
4. Пользователь (Viewer) - Read-only access to vehicles and reports

Usage:
    python manage.py setup_roles
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from cards.models import Vehicle, MaintenanceSchedule, AuditLog, UserProfile


class Command(BaseCommand):
    help = 'Set up role-based access control (RBAC) with 4 groups and permissions'

    def handle(self, *args, **options):
        self.stdout.write(self.style.HTTP_INFO('Initializing role-based access control...'))

        # Get content types for models
        vehicle_ct = ContentType.objects.get_for_model(Vehicle)
        maintenance_ct = ContentType.objects.get_for_model(MaintenanceSchedule)
        auditlog_ct = ContentType.objects.get_for_model(AuditLog)
        userprofile_ct = ContentType.objects.get_for_model(UserProfile)

        # Define permission sets per role
        roles_config = {
            'Администратор': {
                'display_name': 'Администратор',
                'permissions': [
                    # Vehicle permissions
                    ('add_vehicle', vehicle_ct),
                    ('change_vehicle', vehicle_ct),
                    ('delete_vehicle', vehicle_ct),
                    ('view_vehicle', vehicle_ct),
                    # MaintenanceSchedule permissions
                    ('add_maintenanceschedule', maintenance_ct),
                    ('change_maintenanceschedule', maintenance_ct),
                    ('delete_maintenanceschedule', maintenance_ct),
                    ('view_maintenanceschedule', maintenance_ct),
                    # AuditLog permissions
                    ('view_auditlog', auditlog_ct),
                    # UserProfile permissions
                    ('add_userprofile', userprofile_ct),
                    ('change_userprofile', userprofile_ct),
                    ('view_userprofile', userprofile_ct),
                ]
            },
            'Руководитель': {
                'display_name': 'Руководитель',
                'permissions': [
                    # Vehicle permissions - full CRUD
                    ('add_vehicle', vehicle_ct),
                    ('change_vehicle', vehicle_ct),
                    ('delete_vehicle', vehicle_ct),
                    ('view_vehicle', vehicle_ct),
                    # MaintenanceSchedule permissions - full CRUD
                    ('add_maintenanceschedule', maintenance_ct),
                    ('change_maintenanceschedule', maintenance_ct),
                    ('delete_maintenanceschedule', maintenance_ct),
                    ('view_maintenanceschedule', maintenance_ct),
                    # AuditLog - view only
                    ('view_auditlog', auditlog_ct),
                    # UserProfile - view only
                    ('view_userprofile', userprofile_ct),
                ]
            },
            'Специалист': {
                'display_name': 'Специалист',
                'permissions': [
                    # Vehicle - add and change only (no delete)
                    ('add_vehicle', vehicle_ct),
                    ('change_vehicle', vehicle_ct),
                    ('view_vehicle', vehicle_ct),
                    # MaintenanceSchedule - add and change only
                    ('add_maintenanceschedule', maintenance_ct),
                    ('change_maintenanceschedule', maintenance_ct),
                    ('view_maintenanceschedule', maintenance_ct),
                    # AuditLog - view only
                    ('view_auditlog', auditlog_ct),
                    # UserProfile - view only
                    ('view_userprofile', userprofile_ct),
                ]
            },
            'Пользователь': {
                'display_name': 'Пользователь',
                'permissions': [
                    # Vehicle - view only
                    ('view_vehicle', vehicle_ct),
                    # MaintenanceSchedule - view only
                    ('view_maintenanceschedule', maintenance_ct),
                    # AuditLog - view only
                    ('view_auditlog', auditlog_ct),
                    # UserProfile - view only
                    ('view_userprofile', userprofile_ct),
                ]
            },
        }

        # Create groups with permissions
        for role_key, role_config in roles_config.items():
            group, created = Group.objects.get_or_create(name=role_key)

            # Clear existing permissions (for update scenarios)
            group.permissions.clear()

            # Add new permissions
            for perm_codename, content_type in role_config['permissions']:
                try:
                    permission = Permission.objects.get(
                        content_type=content_type,
                        codename=perm_codename
                    )
                    group.permissions.add(permission)
                except Permission.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Warning: Permission {perm_codename} not found for {content_type.model}'
                        )
                    )

            status = 'Created' if created else 'Updated'
            self.stdout.write(
                self.style.SUCCESS(
                    f'[OK] {status} group: "{role_config["display_name"]}" with '
                    f'{group.permissions.count()} permissions'
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                '\n[OK] Role-based access control setup completed successfully!\n'
                'Groups created:\n'
                '  1. Администратор (Admin) - Full access\n'
                '  2. Руководитель (Manager) - Full CRUD on vehicles and maintenance\n'
                '  3. Специалист (Specialist) - Add and edit vehicles/maintenance\n'
                '  4. Пользователь (Viewer) - View-only access\n'
            )
        )

        # Optional note about UserProfile
        self.stdout.write(
            self.style.HTTP_INFO(
                'Note: User roles are defined in UserProfile.position field.\n'
                'You can sync user groups by running: python manage.py sync_user_roles'
            )
        )
