from django.contrib import admin
from django.utils.html import format_html
from .models import Vehicle, BrandModel, Color, VehicleType, Category, FuelType, BodyType, UserProfile, AuditLog, MaintenanceSchedule


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

class MaintenanceScheduleInline(admin.TabularInline):
    """Встроенное редактирование расписания ТО-2 прямо из формы ТС"""
    model = MaintenanceSchedule
    extra = 1
    fields = ('status', 'last_maintenance_date', 'next_maintenance_date', 'next_maintenance_mileage', 'notes')
    ordering = ('-next_maintenance_date',)


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    """
    Конфигурация отображения модели Vehicle в административной части Django.

    Обратите внимание на:
    - `list_display` — колонки в списке записей
    - `search_fields` и `list_filter` — удобные фильтры/поиск в админке
    - `fieldsets` — организация полей в форме редактирования (по блокам/категориям)
    - `readonly_fields` и методы превью — показываем превью изображений и файлов
    - `inlines` — вложенное редактирование (MaintenanceSchedule)
    """

    list_display = ('garage_number', 'brand_model', 'vin', 'pts_type', 'color', 'vehicle_type', 'archive_status')
    list_filter = ('pts_type', 'brand_model', 'color', 'vehicle_type', 'category', 'fuel_type', 'is_archived')
    search_fields = ('garage_number', 'vin', 'brand_model__name')
    ordering = ('-is_archived', 'garage_number')
    inlines = [MaintenanceScheduleInline]

    fieldsets = (
        ('БЛОК 1: ПАСПОРТ ТРАНСПОРТНОГО СРЕДСТВА (ПТС/ЭПТС, VIN, марка, модель)', {
            'fields': (
                ('garage_number', 'vin'),
                ('brand_model', 'color', 'vehicle_type'),
                ('category', 'fuel_type', 'body_type'),
                'photo',
                'photo_preview',
                ('pts_type', 'pts_series', 'pts_number', 'pts_date'),
                'pts_scan',
                'pts_preview',
                ('epts_number', 'epts_date'),
                'epts_scan',
                'epts_preview',
            ),
            'description': 'Основная информация о транспортном средстве, ПТС и ЭПТС'
        }),
        ('БЛОК 2: РЕГИСТРАЦИОННЫЕ ДАННЫЕ ГИБДД', {
            'fields': (
                ('grz_series', 'grz_number', 'grz_date'),
                ('reg_certificate_series', 'reg_certificate_number', 'reg_certificate_date'),
                'reg_certificate_scan',
                ('osago_number', 'osago_date_issued', 'osago_date_expiry', 'osago_cost'),
                'osago_scan',
                ('diagnostic_card_number', 'diagnostic_card_date', 'diagnostic_card_expiry'),
                'diagnostic_card_scan',
            ),
            'classes': ('collapse',),
            'description': 'Данные регистрации в ГИБДД, ОСАГО и диагностическая карта'
        }),
        ('БЛОК 3: ОБЩИЕ ХАРАКТЕРИСТИКИ ТС', {
            'fields': (
                ('mass_kg', 'empty_mass', 'cargo_capacity'),
                ('engine_volume', 'engine_power_hp', 'engine_power_kw'),
                ('engine_model_number', 'chassis_number', 'body_number'),
                ('year_of_manufacture', 'mileage_km', 'motor_hours', 'mileage_type'),
                ('passenger_capacity', 'bus_length', 'bucket_capacity'),
                ('fuel_tank_capacity', 'fuel_grade', 'fuel_consumption_type'),
                ('fuel_consumption_summer_city', 'fuel_consumption_summer_highway'),
                ('fuel_consumption_winter_city', 'fuel_consumption_winter_highway'),
                'fuel_consumption_per_hour',
                ('gbo_present', 'gbo_type', 'gbo_volume', 'gbo_installation_date'),
                ('gbo_cylinders_count', 'gbo_total_capacity', 'gbo_inspection_date', 'gbo_next_inspection_date'),
                'gbo_inspection_scan',
                ('dprg_inspection_date', 'dprg_next_inspection_date'),
                'dprg_inspection_scan',
                ('has_ssmt', 'has_tachograph', 'tachograph_calibration_date', 'tachograph_next_calibration_date'),
                ('has_lifting_equipment', 'initial_cost'),
                ('vehicle_type_for_military', 'vehicle_type_for_tax'),
                ('inventory_number', 'motorpool', 'direction'),
                ('ts_status', 'dismission_date', 'axles_count'),
                ('to2_periodicity',),
            ),
            'classes': ('collapse',),
            'description': 'Технические характеристики, ГБО, тахограф и прочие сведения'
        }),
        ('БЛОК 4: ДОКУМЕНТЫ ПО СРОКАМ И БУХГАЛТЕРСКИЕ ДАННЫЕ', {
            'fields': (
                ('to2_period_days', 'to3_period_days'),
                ('tech_inspection_expiry', 'insurance_expiry'),
                ('okof_code', 'date_in_service'),
                ('depreciation_rate', 'accumulated_depreciation', 'residual_value'),
            ),
            'classes': ('collapse',),
            'description': 'Сроки документов (ТО, техосмотр) и бухгалтерские показатели'
        }),
        ('АРХИВИРОВАНИЕ', {
            'fields': ('is_archived', 'archived_at', 'archived_by'),
            'classes': ('collapse',),
            'description': 'Статус архивирования и дата снятия с учета'
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


# ===== ТЕХНИЧЕСКОЕ ОБСЛУЖИВАНИЕ (ТО-2) =====

@admin.register(MaintenanceSchedule)
class MaintenanceScheduleAdmin(admin.ModelAdmin):
    """
    Администраторский интерфейс для управления расписанием ТО-2.

    Отображает:
    - Связь с ТС
    - История последнего обслуживания (дата и пробег)
    - Дата и пробег следующего обслуживания
    - Статус выполнения (Запланировано, В процессе, Завершено, Просрочено, Отменено)
    - Заметки и результаты
    """
    list_display = ('vehicle', 'status_colored', 'next_maintenance_date', 'last_maintenance_date', 'created_at')
    list_filter = ('status', 'vehicle', 'next_maintenance_date', 'created_at')
    search_fields = ('vehicle__garage_number', 'vehicle__brand_model__name')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-next_maintenance_date',)

    fieldsets = (
        ('ТС и статус', {
            'fields': ('vehicle', 'status')
        }),
        ('История обслуживания', {
            'fields': (
                ('last_maintenance_date', 'last_maintenance_mileage'),
            ),
            'classes': ('collapse',),
            'description': 'Дата и пробег последнего проведённого ТО-2'
        }),
        ('Следующее обслуживание', {
            'fields': (
                ('next_maintenance_date', 'next_maintenance_mileage'),
            ),
            'description': 'Дата и пробег, на который запланировано следующее ТО-2'
        }),
        ('Заметки и результаты', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Системные данные', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def status_colored(self, obj):
        """Отобразить статус с цветной подсветкой"""
        colors = {
            'scheduled': '#0056b3',    # синий
            'in_progress': '#0dcaf0', # голубой
            'completed': '#28a745',   # зелёный
            'overdue': '#dc3545',     # красный
            'cancelled': '#6c757d',   # серый
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_colored.short_description = 'Статус'


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

