import csv
import sys
from io import TextIOWrapper
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group
from cards.models import UserProfile


class Command(BaseCommand):
    """
    Управляющая команда для импорта сотрудников из CSV файла.

    Формат CSV:
    ФИО,Табельный номер,Должность,Логин,Группа

    Пример:
    Иван Иванов,001,Администратор,iivanov,Администратор
    Мария Петрова,002,Специалист,mpetrova,Специалист

    Использование:
    python manage.py import_employees data/employees.csv
    """

    help = 'Импортирует сотрудников из CSV файла. Формат: ФИО,Табельный номер,Должность,Логин,Группа'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file',
            type=str,
            help='Путь к CSV файлу с данными сотрудников'
        )

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']

        try:
            with open(csv_file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                # Проверяем наличие требуемых столбцов
                required_fields = {'ФИО', 'Табельный номер', 'Логин', 'Группа'}
                if not reader.fieldnames or not required_fields.issubset(set(reader.fieldnames)):
                    raise CommandError(
                        f'CSV файл должен содержать столбцы: {", ".join(required_fields)}'
                    )

                created_count = 0
                updated_count = 0
                error_count = 0
                errors = []

                for row_num, row in enumerate(reader, start=2):  # start=2 для учета заголовка
                    try:
                        fio = row.get('ФИО', '').strip()
                        tab_number = row.get('Табельный номер', '').strip()
                        position = row.get('Должность', 'Пользователь').strip()
                        username = row.get('Логин', '').strip()
                        group_name = row.get('Группа', 'Пользователь').strip()

                        # Валидация данных
                        if not fio or not tab_number or not username:
                            errors.append(f'Строка {row_num}: отсутствуют обязательные поля')
                            error_count += 1
                            continue

                        # Получаем или создаем группу
                        group, _ = Group.objects.get_or_create(name=group_name)

                        # Получаем или создаем пользователя
                        user, user_created = User.objects.get_or_create(username=username)
                        user.first_name = fio.split()[0] if fio else ''
                        user.last_name = ' '.join(fio.split()[1:]) if len(fio.split()) > 1 else ''
                        user.save()

                        # Добавляем пользователя в группу
                        if not user.groups.filter(pk=group.pk).exists():
                            user.groups.add(group)

                        # Получаем или создаем профиль
                        profile, profile_created = UserProfile.objects.get_or_create(
                            user=user,
                            defaults={
                                'fio': fio,
                                'tab_number': tab_number,
                                'position': position,
                            }
                        )

                        # Обновляем профиль, если нужно
                        if not profile_created:
                            profile.fio = fio
                            profile.tab_number = tab_number
                            profile.position = position
                            profile.save()
                            updated_count += 1
                        else:
                            created_count += 1

                        self.stdout.write(
                            self.style.SUCCESS(
                                f'{"✓" if user_created else "↻"} {fio} ({username}) - {group_name}'
                            )
                        )

                    except Exception as e:
                        error_count += 1
                        errors.append(f'Строка {row_num}: {str(e)}')
                        self.stdout.write(
                            self.style.ERROR(f'✗ Ошибка в строке {row_num}: {str(e)}')
                        )

        except FileNotFoundError:
            raise CommandError(f'Файл не найден: {csv_file_path}')
        except Exception as e:
            raise CommandError(f'Ошибка при чтении файла: {str(e)}')

        # Итоговый отчет
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS(f'Создано: {created_count}'))
        self.stdout.write(self.style.WARNING(f'Обновлено: {updated_count}'))
        self.stdout.write(self.style.ERROR(f'Ошибок: {error_count}'))

        if errors:
            self.stdout.write('\n' + self.style.ERROR('Детали ошибок:'))
            for error in errors:
                self.stdout.write(self.style.ERROR(f'  - {error}'))
