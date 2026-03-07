"""
Management command to sync UserProfile roles with Django user groups.

When a UserProfile.position is changed, this command ensures the user
is assigned to the correct permission group.

Usage:
    python manage.py sync_user_roles [--user <username>]
    python manage.py sync_user_roles  # Sync all users
"""

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group
from cards.models import UserProfile


class Command(BaseCommand):
    help = 'Sync UserProfile roles with Django user groups'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user',
            type=str,
            help='Sync only a specific user (by username)'
        )

    def handle(self, *args, **options):
        user_filter = options.get('user')

        # Role mapping from UserProfile.position to Group name
        role_mapping = {
            'admin': 'Администратор',
            'supervisor': 'Руководитель',
            'specialist': 'Специалист',
            'user': 'Пользователь',
        }

        # Get all groups
        try:
            groups = {name: Group.objects.get(name=name) for name in role_mapping.values()}
        except Group.DoesNotExist as e:
            raise CommandError(
                f'Group not found: {e}. Please run setup_roles command first.\n'
                'Usage: python manage.py setup_roles'
            )

        # Get user profiles to sync
        if user_filter:
            profiles = UserProfile.objects.filter(user__username=user_filter)
            if not profiles.exists():
                raise CommandError(f'User not found: {user_filter}')
        else:
            profiles = UserProfile.objects.all()

        synced_count = 0
        for profile in profiles:
            user = profile.user
            position = profile.position

            # Get target group
            target_group_name = role_mapping.get(position)
            if not target_group_name:
                self.stdout.write(
                    self.style.WARNING(
                        f'Unknown position for {user.username}: {position}'
                    )
                )
                continue

            target_group = groups[target_group_name]

            # Remove user from all other role groups
            for group in groups.values():
                if group != target_group:
                    group.user_set.remove(user)

            # Add user to correct group
            target_group.user_set.add(user)
            synced_count += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f'[OK] {user.username} ({profile.fio}) -> {target_group_name}'
                )
            )

        self.stdout.write(
            self.style.SUCCESS(f'\n[OK] Synced {synced_count} user(s) successfully!')
        )
