import logging
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Vehicle, AuditLog
from .middleware import get_current_user, get_current_ip

# Настройка логирования в файл
audit_logger = logging.getLogger('audit')

# Словарь для сравнения изменений
_vehicle_initial_state = {}


def get_user_fio_and_username(user):
    """Получить ФИО пользователя из профиля или использовать логин"""
    try:
        if hasattr(user, 'profile') and user.profile:
            return user.profile.fio, user.username
    except:
        pass
    return user.username if user else "Unknown", user.username if user else "unknown"


def log_action(user, action, obj, changes=None, ip_address=None):
    """
    Логирует действие в базе данных и в файле журнала

    Args:
        user: объект User
        action: тип действия ('CREATE', 'UPDATE', 'DELETE', 'VIEW')
        obj: объект модели (Vehicle)
        changes: описание изменений (для UPDATE)
        ip_address: IP адрес клиента
    """
    if not user or not user.is_authenticated:
        return

    user_fio, username = get_user_fio_and_username(user)

    # Описание объекта
    object_description = str(obj)

    # Запись в БД
    AuditLog.objects.create(
        user_fio=user_fio,
        username=username,
        action=action,
        model_name=obj.__class__.__name__,
        object_id=obj.id if obj.id else 0,
        object_description=object_description,
        changes=changes or '',
        ip_address=ip_address
    )

    # Логирование в файл
    log_message = f"{action:10} | {user_fio:30} | {object_description:50} | {changes or '-'}"
    audit_logger.info(log_message)


@receiver(pre_save, sender=Vehicle)
def vehicle_pre_save(sender, instance, **kwargs):
    """Сохраняет исходное состояние перед обновлением"""
    if instance.pk:
        try:
            _vehicle_initial_state[instance.pk] = Vehicle.objects.get(pk=instance.pk)
        except Vehicle.DoesNotExist:
            pass


@receiver(post_save, sender=Vehicle)
def vehicle_post_save(sender, instance, created, using, **kwargs):
    """
    Логирует создание или обновление транспортного средства.

    Сигнал срабатывает после сохранения объекта в БД.
    """
    # Получаем пользователя из thread-local контекста middleware
    user = get_current_user()

    if not user or not user.is_authenticated:
        return

    ip_address = get_current_ip()

    if created:
        action = 'CREATE'
        changes = f"Создано новое ТС: {instance}"
    else:
        action = 'UPDATE'
        # Сравниваем с исходным состоянием
        initial = _vehicle_initial_state.get(instance.pk)
        if initial:
            changes_list = []
            for field in instance._meta.fields:
                initial_value = getattr(initial, field.name, None)
                current_value = getattr(instance, field.name, None)
                if initial_value != current_value:
                    changes_list.append(
                        f"{field.verbose_name}: '{initial_value}' -> '{current_value}'"
                    )
            changes = "; ".join(changes_list) if changes_list else "Без видимых изменений"
            # Очищаем кэш после обработки
            if instance.pk in _vehicle_initial_state:
                del _vehicle_initial_state[instance.pk]
        else:
            changes = "Обновлено"

    log_action(user, action, instance, changes, ip_address)


@receiver(post_delete, sender=Vehicle)
def vehicle_post_delete(sender, instance, using, **kwargs):
    """
    Логирует удаление транспортного средства.

    Сигнал срабатывает после удаления объекта из БД.
    """
    user = get_current_user()

    if not user or not user.is_authenticated:
        return

    ip_address = get_current_ip()
    changes = f"Удалено ТС: {instance}"

    log_action(user, 'DELETE', instance, changes, ip_address)

