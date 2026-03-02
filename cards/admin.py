from django.contrib import admin
from django.utils.html import format_html
from .models import Vehicle, BrandModel, Color, VehicleType, Category, FuelType, BodyType, UserProfile, AuditLog


# ===== ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ =====

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('fio', 'tab_number', 'position', 'user')
    list_filter = ('position', 'created_at')
    search_fields = ('fio', 'tab_number', 'user__username')
    ordering = ('fio',)

    fieldsets = (
        ('Основные данные', {
            'fields': ('user', 'fio', 'tab_number', 'position')
        }),
        ('Системные данные', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('created_at', 'updated_at')


# ===== СПРАВОЧНЫЕ МОДЕЛИ =====

@admin.register(BrandModel)
class BrandModelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(VehicleType)
class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(FuelType)
class FuelTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(BodyType)
class BodyTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


# ===== ОСНОВНАЯ МОДЕЛЬ =====

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    """
    Конфигурация отображения модели Vehicle в административной части Django.

    Обратите внимание на:
    - `list_display` — колонки в списке записей
    - `search_fields` и `list_filter` — удобные фильтры/поиск в админке
    - `fieldsets` — организация полей в форме редактирования (по блокам/категориям)
    - `readonly_fields` и методы превью — показываем превью изображений и файлов
    """

    list_display = ('garage_number', 'brand_model', 'vin', 'pts_type', 'color', 'vehicle_type', 'archive_status')
    list_filter = ('pts_type', 'brand_model', 'color', 'vehicle_type', 'category', 'fuel_type', 'is_archived')
    search_fields = ('garage_number', 'vin', 'brand_model__name')
    ordering = ('-is_archived', 'garage_number')

    fieldsets = (
        ('Основные реквизиты', {
            'fields': ('garage_number', 'brand_model', 'vin', 'photo', 'photo_preview')
        }),
        ('Характеристики', {
            'fields': ('color', 'vehicle_type', 'category', 'fuel_type', 'body_type',
                      'mass_kg', 'mileage_km', 'engine_volume', 'engine_power_hp', 'axles_count'),
            'classes': ('collapse',)
        }),
        ('Паспорт транспортного средства (ПТС)', {
            'fields': ('pts_type', 'pts_series', 'pts_number', 'pts_date', 'pts_scan', 'pts_preview'),
            'classes': ('collapse',)
        }),
        ('Электронный паспорт (ЭПТС)', {
            'fields': ('epts_number', 'epts_date', 'epts_scan', 'epts_preview'),
            'classes': ('collapse',)
        }),
        ('Регистрационные данные ГИБДД', {
            'fields': (
                ('grz_series', 'grz_number', 'grz_date'),
                ('reg_certificate_series', 'reg_certificate_number', 'reg_certificate_date', 'reg_certificate_scan'),
                ('osago_number', 'osago_date_issued', 'osago_date_expiry', 'osago_scan'),
                ('diagnostic_card_number', 'diagnostic_card_date', 'diagnostic_card_expiry', 'diagnostic_card_scan')
            ),
            'classes': ('collapse',)
        }),
        ('ГБО (газобаллонное оборудование)', {
            'fields': ('gbo_present', 'gbo_type', 'gbo_volume', 'gbo_installation_date'),
            'classes': ('collapse',)
        }),
        ('Документы по срокам', {
            'fields': ('to2_period_days', 'to3_period_days', 'tech_inspection_expiry', 'insurance_expiry'),
            'classes': ('collapse',)
        }),
        ('Архивирование', {
            'fields': ('is_archived', 'archived_at', 'archived_by'),
            'classes': ('collapse',)
        }),
    )

    # Поля только для чтения (они будут отображаться как превью)
    readonly_fields = ('photo_preview', 'pts_preview', 'epts_preview', 'archived_at', 'archived_by')

    def photo_preview(self, obj):
        """Превью фотографии ТС"""
        if obj.photo:
            return format_html(
                '<img src="{}" style="max-height: 200px; border-radius: 8px;">',
                obj.photo.url
            )
        return "(нет фото)"
    photo_preview.short_description = "Превью фото"

    def pts_preview(self, obj):
        """Превью скана ПТС (если PDF/изображение)"""
        if obj.pts_scan:
            file_url = obj.pts_scan.url
            if file_url.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                return format_html(
                    '<img src="{}" style="max-height: 200px; border-radius: 8px;">',
                    file_url
                )
            else:
                # Для PDF и других файлов показываем ссылку для скачивания
                return format_html(
                    '<a href="{}" target="_blank" download>{}</a>',
                    file_url,
                    obj.pts_scan.name
                )
        return "(нет скана)"
    pts_preview.short_description = "Превью ПТС"

    def epts_preview(self, obj):
        """Превью скана ЭПТС (если PDF/изображение)"""
        if obj.epts_scan:
            file_url = obj.epts_scan.url
            if file_url.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                return format_html(
                    '<img src="{}" style="max-height: 200px; border-radius: 8px;">',
                    file_url
                )
            else:
                # Для PDF и других файлов показываем ссылку для скачивания
                return format_html(
                    '<a href="{}" target="_blank" download>{}</a>',
                    file_url,
                    obj.epts_scan.name
                )
        return "(нет скана)"
    epts_preview.short_description = "Превью ЭПТС"

    def archive_status(self, obj):
        """Показать статус архивирования с цветным индикатором"""
        if obj.is_archived:
            return format_html(
                '<span style="background-color: #ffc107; color: #000; padding: 5px 10px; border-radius: 3px; font-weight: bold;">АРХИВ</span>'
            )
        else:
            return format_html(
                '<span style="background-color: #28a745; color: #fff; padding: 5px 10px; border-radius: 3px; font-weight: bold;">АКТИВНО</span>'
            )
    archive_status.short_description = "Статус архива"


# ===== АУДИТ-ЛОГИРОВАНИЕ =====

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """
    Администраторский интерфейс для просмотра журнала аудита.

    Отображает все записи со следующей информацией:
    - ФИО пользователя
    - Тип действия (CREATE, UPDATE, DELETE)
    - Описание объекта
    - Дата и время
    - Внесённые изменения
    """
    list_display = ('timestamp', 'user_fio', 'action_colored', 'object_description', 'model_name')
    list_filter = ('action', 'model_name', 'timestamp', 'user_fio')
    search_fields = ('user_fio', 'username', 'object_description')
    readonly_fields = ('timestamp', 'user_fio', 'username', 'action', 'model_name', 'object_id', 'object_description', 'changes', 'ip_address')
    ordering = ('-timestamp',)

    fieldsets = (
        ('Информация о действии', {
            'fields': ('timestamp', 'action', 'user_fio', 'username', 'ip_address')
        }),
        ('Информация об объекте', {
            'fields': ('model_name', 'object_id', 'object_description')
        }),
        ('Изменения', {
            'fields': ('changes',),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        """Запретить добавление записей вручную"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Запретить удаление записей (для сохранения целостности журнала)"""
        return False

    def has_change_permission(self, request, obj=None):
        """Запретить изменение записей"""
        return False

    def action_colored(self, obj):
        """Отобразить действие с цветной подсветкой"""
        colors = {
            'CREATE': '#28a745',  # зелёный
            'UPDATE': '#ffc107',  # жёлтый
            'DELETE': '#dc3545',  # красный
            'VIEW': '#17a2b8',    # голубой
        }
        color = colors.get(obj.action, '#6c757d')  # серый по умолчанию
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_action_display()
        )
    action_colored.short_description = 'Действие'

