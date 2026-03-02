from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from .models import Vehicle, AuditLog


class VehicleListView(LoginRequiredMixin, ListView):
    """
    Список всех транспортных средств с поиском и пагинацией.

    Поиск работает по:
    - Гаражному номеру
    - VIN номеру
    - Государственному регистрационному номеру (ГРЗ)
    - Марке и модели
    - Номеру полиса ОСАГО
    - Номеру диагностической карты
    (все поиски нечувствительны к регистру)

    Требует аутентификации.
    """
    model = Vehicle
    template_name = 'cards/vehicle_list.html'
    context_object_name = 'vehicles'
    paginate_by = 10
    login_url = 'admin:login'

    def get_queryset(self):
        # Переопределяем queryset, чтобы добавить фильтрацию по поисковому запросу
        queryset = super().get_queryset().filter(is_archived=False)
        q = self.request.GET.get('q')
        if q:
            # Расширенный поиск по множеству полей
            queryset = queryset.filter(
                Q(garage_number__icontains=q) |           # Гаражный номер
                Q(vin__icontains=q) |                     # VIN номер
                Q(grz_number__icontains=q) |              # Номер ГРЗ (АА123БВ)
                Q(grz_series__icontains=q) |              # Серия ГРЗ (78)
                Q(brand_model__name__icontains=q) |       # Марка и модель
                Q(osago_number__icontains=q) |            # Номер ОСАГО
                Q(diagnostic_card_number__icontains=q) |  # Номер диагностической карты
                Q(reg_certificate_number__icontains=q)    # Номер свидетельства регистрации
            )
        return queryset


class VehicleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Форма создания нового транспортного средства.

    Только для пользователей в группах: Администратор, Специалист
    """
    model = Vehicle
    template_name = 'cards/vehicle_form.html'
    fields = [
        # Основные реквизиты
        'garage_number', 'brand_model', 'vin', 'photo',
        # Характеристики кузова
        'color', 'vehicle_type', 'category', 'fuel_type', 'body_type',
        # Паспорт ТС
        'pts_type', 'pts_series', 'pts_number', 'pts_date', 'pts_scan',
        'epts_number', 'epts_date', 'epts_scan',
        # Регистрационные данные ГИБДД
        'grz_series', 'grz_number', 'grz_date',
        'reg_certificate_series', 'reg_certificate_number', 'reg_certificate_date', 'reg_certificate_scan',
        'osago_number', 'osago_date_issued', 'osago_date_expiry', 'osago_cost', 'osago_scan',
        'diagnostic_card_number', 'diagnostic_card_date', 'diagnostic_card_expiry', 'diagnostic_card_scan',
        # Техническое снятие с учета
        'dismission_date',
        # Характеристики двигателя
        'engine_volume', 'engine_power_hp', 'engine_power_kw', 'engine_model_number',
        # Номера конструктивных элементов
        'chassis_number', 'body_number',
        # Год выпуска и характеристики
        'year_of_manufacture', 'axles_count',
        # Масса и грузоподъемность
        'mass_kg', 'empty_mass', 'cargo_capacity', 'passenger_capacity',
        # Габариты и емкости
        'bus_length', 'bucket_capacity', 'fuel_tank_capacity',
        # Топливо
        'fuel_grade', 'fuel_consumption_type',
        'fuel_consumption_summer_city', 'fuel_consumption_summer_highway',
        'fuel_consumption_winter_city', 'fuel_consumption_winter_highway',
        'fuel_consumption_per_hour',
        # Классификация для разных ведомств
        'vehicle_type_for_military', 'vehicle_type_for_tax', 'initial_cost',
        # Общие данные и статус
        'inventory_number', 'motorpool', 'direction', 'ts_status',
        # Пробег и моточасы
        'mileage_km', 'mileage_type', 'motor_hours', 'to2_periodicity',
        # ГБО (газобаллонное оборудование)
        'gbo_present', 'gbo_type', 'gbo_volume', 'gbo_installation_date',
        'gbo_cylinders_count', 'gbo_total_capacity',
        'gbo_inspection_date', 'gbo_next_inspection_date', 'gbo_inspection_scan',
        # ССМТ и другое оборудование
        'has_ssmt', 'has_tachograph',
        'tachograph_calibration_date', 'tachograph_next_calibration_date',
        'has_lifting_equipment',
        # Техническое обслуживание
        'dprg_inspection_date', 'dprg_next_inspection_date', 'dprg_inspection_scan',
        # Бухгалтерские данные
        'okof_code', 'date_in_service', 'depreciation_rate',
        'accumulated_depreciation', 'residual_value',
        # Старые поля сроков (для совместимости)
        'to2_period_days', 'to3_period_days', 'tech_inspection_expiry', 'insurance_expiry'
    ]
    login_url = 'admin:login'

    def test_func(self):
        """Проверка: может ли пользователь редактировать"""
        groups = [g.name for g in self.request.user.groups.all()]
        return 'Администратор' in groups or 'Специалист' in groups or 'Руководитель' in groups


class VehicleDetailView(LoginRequiredMixin, DetailView):
    """
    Подробный просмотр одного транспортного средства.

    Отображает все реквизиты карточки со ссылками на редактирование и удаление
    (в зависимости от прав пользователя).
    """
    model = Vehicle
    template_name = 'cards/vehicle_detail.html'
    context_object_name = 'vehicle'
    login_url = 'admin:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем информацию о правах в контекст
        groups = [g.name for g in self.request.user.groups.all()]
        context['can_edit'] = 'Администратор' in groups or 'Специалист' in groups or 'Руководитель' in groups
        context['can_delete'] = 'Администратор' in groups or 'Руководитель' in groups
        return context


class VehicleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Форма редактирования существующего транспортного средства.

    Только для пользователей в группах: Администратор, Специалист, Руководитель
    """
    model = Vehicle
    template_name = 'cards/vehicle_form.html'
    fields = [
        # Основные реквизиты
        'garage_number', 'brand_model', 'vin', 'photo',
        # Характеристики кузова
        'color', 'vehicle_type', 'category', 'fuel_type', 'body_type',
        # Паспорт ТС
        'pts_type', 'pts_series', 'pts_number', 'pts_date', 'pts_scan',
        'epts_number', 'epts_date', 'epts_scan',
        # Регистрационные данные ГИБДД
        'grz_series', 'grz_number', 'grz_date',
        'reg_certificate_series', 'reg_certificate_number', 'reg_certificate_date', 'reg_certificate_scan',
        'osago_number', 'osago_date_issued', 'osago_date_expiry', 'osago_cost', 'osago_scan',
        'diagnostic_card_number', 'diagnostic_card_date', 'diagnostic_card_expiry', 'diagnostic_card_scan',
        # Техническое снятие с учета
        'dismission_date',
        # Характеристики двигателя
        'engine_volume', 'engine_power_hp', 'engine_power_kw', 'engine_model_number',
        # Номера конструктивных элементов
        'chassis_number', 'body_number',
        # Год выпуска и характеристики
        'year_of_manufacture', 'axles_count',
        # Масса и грузоподъемность
        'mass_kg', 'empty_mass', 'cargo_capacity', 'passenger_capacity',
        # Габариты и емкости
        'bus_length', 'bucket_capacity', 'fuel_tank_capacity',
        # Топливо
        'fuel_grade', 'fuel_consumption_type',
        'fuel_consumption_summer_city', 'fuel_consumption_summer_highway',
        'fuel_consumption_winter_city', 'fuel_consumption_winter_highway',
        'fuel_consumption_per_hour',
        # Классификация для разных ведомств
        'vehicle_type_for_military', 'vehicle_type_for_tax', 'initial_cost',
        # Общие данные и статус
        'inventory_number', 'motorpool', 'direction', 'ts_status',
        # Пробег и моточасы
        'mileage_km', 'mileage_type', 'motor_hours', 'to2_periodicity',
        # ГБО (газобаллонное оборудование)
        'gbo_present', 'gbo_type', 'gbo_volume', 'gbo_installation_date',
        'gbo_cylinders_count', 'gbo_total_capacity',
        'gbo_inspection_date', 'gbo_next_inspection_date', 'gbo_inspection_scan',
        # ССМТ и другое оборудование
        'has_ssmt', 'has_tachograph',
        'tachograph_calibration_date', 'tachograph_next_calibration_date',
        'has_lifting_equipment',
        # Техническое обслуживание
        'dprg_inspection_date', 'dprg_next_inspection_date', 'dprg_inspection_scan',
        # Бухгалтерские данные
        'okof_code', 'date_in_service', 'depreciation_rate',
        'accumulated_depreciation', 'residual_value',
        # Старые поля сроков (для совместимости)
        'to2_period_days', 'to3_period_days', 'tech_inspection_expiry', 'insurance_expiry'
    ]
    success_url = reverse_lazy('cards:vehicle_list')
    login_url = 'admin:login'

    def test_func(self):
        """Проверка: может ли пользователь редактировать"""
        groups = [g.name for g in self.request.user.groups.all()]
        return 'Администратор' in groups or 'Специалист' in groups or 'Руководитель' in groups


class VehicleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Удаление транспортного средства с подтверждением.

    Только для пользователей в группах: Администратор, Руководитель
    """
    model = Vehicle
    template_name = 'cards/vehicle_confirm_delete.html'
    success_url = reverse_lazy('cards:vehicle_list')
    login_url = 'admin:login'

    def test_func(self):
        """Проверка: может ли пользователь удалять"""
        groups = [g.name for g in self.request.user.groups.all()]
        return 'Администратор' in groups or 'Руководитель' in groups


class VehicleExportView(LoginRequiredMixin, View):
    """
    Экспорт списка транспортных средств в Excel.

    Поддерживает фильтрацию по поисковому запросу 'q' (аналогично VehicleListView).
    Требует аутентификации.
    """
    login_url = 'admin:login'

    def get_queryset(self):
        """Получить отфильтрованный список ТС (с учётом поиска)"""
        queryset = Vehicle.objects.all()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(garage_number__icontains=q) |
                Q(vin__icontains=q) |
                Q(grz_number__icontains=q) |
                Q(grz_series__icontains=q) |
                Q(brand_model__name__icontains=q) |
                Q(osago_number__icontains=q) |
                Q(diagnostic_card_number__icontains=q) |
                Q(reg_certificate_number__icontains=q)
            )
        return queryset.order_by('garage_number')

    def get(self, request, *args, **kwargs):
        """Генерирует Excel файл и возвращает его как ответ"""
        vehicles = self.get_queryset()

        # Создаём новую рабочую книгу
        wb = Workbook()
        ws = wb.active
        ws.title = "Транспортные средства"

        # Стили
        header_font = Font(bold=True, color="FFFFFF", size=11)
        header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
        header_alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )

        # Заголовки колонок
        headers = [
            "Гаражный номер",
            "Марка и модель",
            "VIN",
            "Цвет",
            "Тип кузова",
            "Тип топлива",
            "Категория",
            "Масса (кг)",
            "Пробег (км)",
            "Объем двигателя (л)",
            "Мощность (л.с.)",
            "Осей",
            "ПТС/ЭПТС",
            "ГРЗ",
            "ОСАГО (номер)",
            "ОСАГО (до)",
            "Диагностическая карта (номер)",
            "Диагностическая карта (до)",
            "Техосмотр (до)",
            "Статус документов"
        ]

        # Вписываем заголовки в первую строку
        for col_idx, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col_idx)
            cell.value = header
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = header_alignment
            cell.border = border

        # Вписываем данные
        for row_idx, vehicle in enumerate(vehicles, 2):
            data = [
                vehicle.garage_number,
                str(vehicle.brand_model),
                vehicle.vin,
                str(vehicle.color) if vehicle.color else "",
                str(vehicle.body_type) if vehicle.body_type else "",
                str(vehicle.fuel_type) if vehicle.fuel_type else "",
                str(vehicle.category) if vehicle.category else "",
                vehicle.mass_kg or "",
                vehicle.mileage_km or "",
                vehicle.engine_volume or "",
                vehicle.engine_power_hp or "",
                vehicle.axles_count or "",
                vehicle.get_pts_type_display() if vehicle.pts_type else "",
                f"{vehicle.grz_series}{vehicle.grz_number}" if vehicle.grz_series and vehicle.grz_number else "",
                vehicle.osago_number or "",
                vehicle.osago_date_expiry.strftime("%d.%m.%Y") if vehicle.osago_date_expiry else "",
                vehicle.diagnostic_card_number or "",
                vehicle.diagnostic_card_expiry.strftime("%d.%m.%Y") if vehicle.diagnostic_card_expiry else "",
                vehicle.tech_inspection_expiry.strftime("%d.%m.%Y") if vehicle.tech_inspection_expiry else "",
                vehicle.get_expiry_status()[1]  # Текстовое описание статуса
            ]

            for col_idx, value in enumerate(data, 1):
                cell = ws.cell(row=row_idx, column=col_idx)
                cell.value = value
                cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
                cell.border = border

        # Автоматическая ширина колонок
        ws.column_dimensions['A'].width = 14
        ws.column_dimensions['B'].width = 20
        ws.column_dimensions['C'].width = 17
        ws.column_dimensions['D'].width = 12
        ws.column_dimensions['E'].width = 14
        ws.column_dimensions['F'].width = 12
        ws.column_dimensions['G'].width = 12
        ws.column_dimensions['H'].width = 12
        ws.column_dimensions['I'].width = 12
        ws.column_dimensions['J'].width = 12
        ws.column_dimensions['K'].width = 12
        ws.column_dimensions['L'].width = 10
        ws.column_dimensions['M'].width = 12
        ws.column_dimensions['N'].width = 12
        ws.column_dimensions['O'].width = 14
        ws.column_dimensions['P'].width = 14
        ws.column_dimensions['Q'].width = 18
        ws.column_dimensions['R'].width = 18
        ws.column_dimensions['S'].width = 14
        ws.column_dimensions['T'].width = 20

        # Высота строки заголовка
        ws.row_dimensions[1].height = 28

        # Возвращаем файл как HTTP ответ
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        response['Content-Disposition'] = f'attachment; filename="vehicles_{timestamp}.xlsx"'
        wb.save(response)
        return response


class VehicleArchiveView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Архивирование транспортного средства.

    Только для пользователей в группах: Администратор, Руководитель
    """
    login_url = 'admin:login'

    def test_func(self):
        """Проверка: может ли пользователь архивировать"""
        groups = [g.name for g in self.request.user.groups.all()]
        return 'Администратор' in groups or 'Руководитель' in groups

    def post(self, request, pk, *args, **kwargs):
        """Архивирует ТС и логирует действие"""
        try:
            vehicle = Vehicle.objects.get(pk=pk)
            vehicle.is_archived = True
            vehicle.archived_at = timezone.now()
            vehicle.archived_by = request.user
            vehicle.save()

            # Логируем архивирование
            AuditLog.objects.create(
                user_fio=request.user.profile.fio if hasattr(request.user, 'profile') and request.user.profile else request.user.username,
                username=request.user.username,
                action='UPDATE',
                model_name='Vehicle',
                object_id=vehicle.id,
                object_description=str(vehicle),
                changes='Архивировано (снято с учета)',
                ip_address=self._get_client_ip(request)
            )

            return JsonResponse({'status': 'success', 'message': 'ТС архивировано'})
        except Vehicle.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'ТС не найдено'}, status=404)

    def _get_client_ip(self, request):
        """Получить IP адрес клиента"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class VehicleUnarchiveView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Восстановление транспортного средства из архива.

    Только для пользователей в группах: Администратор, Руководитель
    """
    login_url = 'admin:login'

    def test_func(self):
        """Проверка: может ли пользователь восстанавливать из архива"""
        groups = [g.name for g in self.request.user.groups.all()]
        return 'Администратор' in groups or 'Руководитель' in groups

    def post(self, request, pk, *args, **kwargs):
        """Восстанавливает ТС из архива и логирует действие"""
        try:
            vehicle = Vehicle.objects.get(pk=pk)
            vehicle.is_archived = False
            vehicle.archived_at = None
            vehicle.archived_by = None
            vehicle.save()

            # Логируем восстановление
            AuditLog.objects.create(
                user_fio=request.user.profile.fio if hasattr(request.user, 'profile') and request.user.profile else request.user.username,
                username=request.user.username,
                action='UPDATE',
                model_name='Vehicle',
                object_id=vehicle.id,
                object_description=str(vehicle),
                changes='Восстановлено из архива (возвращено в учет)',
                ip_address=self._get_client_ip(request)
            )

            return JsonResponse({'status': 'success', 'message': 'ТС восстановлено'})
        except Vehicle.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'ТС не найдено'}, status=404)

    def _get_client_ip(self, request):
        """Получить IP адрес клиента"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

