"""
Django forms for the vehicle management system.

Organized by 4 logical blocks:
1. Паспорт ТС (Vehicle Passport) - Basic identification and documents
2. Регистрационные данные ГИБДД (Registration) - Legal registration and insurance
3. Общие характеристики (Common characteristics) - Technical specifications
4. Документы по срокам (Document expiry dates) - Maintenance and legal deadlines
"""

from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Vehicle, MaintenanceSchedule


class VehicleForm(forms.ModelForm):
    """
    Form for creating and editing Vehicle records with 4-block structure.

    The form groups related fields into logical fieldsets for better UX:
    - Block 1: Passport (VIN, garage number, brand, PTS/EPTS docs)
    - Block 2: Registration (GIBDD registration, OSAGO, diagnostic card)
    - Block 3: Common characteristics (Engine, fuel, capacity, etc.)
    - Block 4: Document expiry dates (Tech inspection, insurance, maintenance)
    """

    class Meta:
        model = Vehicle
        fields = [
            # BLOCK 1: ПАСПОРТ ТРАНСПОРТНОГО СРЕДСТВА
            'garage_number', 'vin', 'brand_model', 'color', 'vehicle_type',
            'category', 'fuel_type', 'body_type', 'photo',
            'pts_type', 'pts_series', 'pts_number', 'pts_date', 'pts_scan',
            'epts_number', 'epts_date', 'epts_scan',

            # BLOCK 2: РЕГИСТРАЦИОННЫЕ ДАННЫЕ ГИБДД
            'grz_series', 'grz_number', 'grz_date',
            'reg_certificate_series', 'reg_certificate_number', 'reg_certificate_date', 'reg_certificate_scan',
            'osago_number', 'osago_date_issued', 'osago_date_expiry', 'osago_cost', 'osago_scan',
            'diagnostic_card_number', 'diagnostic_card_date', 'diagnostic_card_expiry', 'diagnostic_card_scan',

            # BLOCK 3: ОБЩИЕ ХАРАКТЕРИСТИКИ
            'mass_kg', 'empty_mass', 'cargo_capacity',
            'engine_volume', 'engine_power_hp', 'engine_power_kw',
            'engine_model_number', 'chassis_number', 'body_number',
            'year_of_manufacture', 'mileage_km', 'motor_hours', 'mileage_type',
            'passenger_capacity', 'bus_length', 'bucket_capacity',
            'fuel_tank_capacity', 'fuel_grade', 'fuel_consumption_type',
            'fuel_consumption_summer_city', 'fuel_consumption_summer_highway',
            'fuel_consumption_winter_city', 'fuel_consumption_winter_highway',
            'fuel_consumption_per_hour',
            'gbo_present', 'gbo_type', 'gbo_volume', 'gbo_installation_date',
            'gbo_cylinders_count', 'gbo_total_capacity', 'gbo_inspection_date', 'gbo_next_inspection_date',
            'gbo_inspection_scan',
            'dprg_inspection_date', 'dprg_next_inspection_date', 'dprg_inspection_scan',
            'has_ssmt', 'has_tachograph', 'tachograph_calibration_date', 'tachograph_next_calibration_date',
            'has_lifting_equipment', 'initial_cost',
            'vehicle_type_for_military', 'vehicle_type_for_tax',
            'inventory_number', 'motorpool', 'direction',
            'ts_status', 'dismission_date', 'axles_count',
            'to2_periodicity',

            # BLOCK 4: ДОКУМЕНТЫ ПО СРОКАМ И БУХГАЛТЕРСКИЕ ДАННЫЕ
            'to2_period_days', 'to3_period_days',
            'tech_inspection_expiry', 'insurance_expiry',
            'okof_code', 'date_in_service',
            'depreciation_rate', 'accumulated_depreciation', 'residual_value',

            # ARCHIVE
            'is_archived',
        ]

        widgets = {
            # Text inputs
            'garage_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: 0101',
                'maxlength': '20'
            }),
            'vin': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'VIN код (17 символов)',
                'maxlength': '17'
            }),
            'pts_series': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: 78РС',
                'maxlength': '4'
            }),
            'pts_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '6 цифр',
                'maxlength': '6'
            }),
            'epts_number': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '20'
            }),
            'grz_series': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: 78',
                'maxlength': '2'
            }),
            'grz_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: АА123БВ',
                'maxlength': '6'
            }),
            'reg_certificate_series': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '4'
            }),
            'reg_certificate_number': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '6'
            }),
            'osago_number': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '20'
            }),
            'diagnostic_card_number': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '20'
            }),
            'engine_model_number': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '50'
            }),
            'chassis_number': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '50'
            }),
            'body_number': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '50'
            }),
            'year_of_manufacture': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ГГГГ',
                'maxlength': '4'
            }),
            'inventory_number': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '20'
            }),
            'motorpool': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '01, 02, 03...',
                'maxlength': '10'
            }),
            'direction': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '1'
            }),
            'gbo_type': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '50'
            }),
            'fuel_grade': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '50'
            }),
            'ts_status': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '50'
            }),
            'okof_code': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '20'
            }),

            # Decimal and Integer inputs
            'mass_kg': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'empty_mass': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'cargo_capacity': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'engine_volume': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'engine_power_hp': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'engine_power_kw': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'mileage_km': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'motor_hours': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'passenger_capacity': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'bus_length': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.001'
            }),
            'bucket_capacity': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.001'
            }),
            'fuel_tank_capacity': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.001'
            }),
            'fuel_consumption_summer_city': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'fuel_consumption_summer_highway': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'fuel_consumption_winter_city': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'fuel_consumption_winter_highway': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'fuel_consumption_per_hour': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'gbo_volume': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'gbo_cylinders_count': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'gbo_total_capacity': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.001'
            }),
            'initial_cost': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'osago_cost': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'axles_count': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'to2_periodicity': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'to2_period_days': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'to3_period_days': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'depreciation_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'accumulated_depreciation': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'residual_value': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),

            # Date inputs
            'pts_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'epts_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'grz_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'reg_certificate_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'osago_date_issued': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'osago_date_expiry': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'diagnostic_card_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'diagnostic_card_expiry': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'gbo_installation_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'gbo_inspection_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'gbo_next_inspection_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'dprg_inspection_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'dprg_next_inspection_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'tachograph_calibration_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'tachograph_next_calibration_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'dismission_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'date_in_service': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'tech_inspection_expiry': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'insurance_expiry': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            # File inputs
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'pts_scan': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'epts_scan': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'reg_certificate_scan': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'osago_scan': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'diagnostic_card_scan': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'gbo_inspection_scan': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'dprg_inspection_scan': forms.FileInput(attrs={
                'class': 'form-control'
            }),

            # Choice fields
            'pts_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'mileage_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'fuel_consumption_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'vehicle_type_for_military': forms.Select(attrs={
                'class': 'form-select'
            }),
            'vehicle_type_for_tax': forms.Select(attrs={
                'class': 'form-select'
            }),

            # ForeignKey fields
            'brand_model': forms.Select(attrs={
                'class': 'form-select'
            }),
            'color': forms.Select(attrs={
                'class': 'form-select'
            }),
            'vehicle_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'fuel_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'body_type': forms.Select(attrs={
                'class': 'form-select'
            }),

            # Boolean fields
            'gbo_present': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'has_ssmt': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'has_tachograph': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'has_lifting_equipment': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_archived': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

        labels = {
            # BLOCK 1
            'garage_number': _('Гаражный номер'),
            'vin': _('VIN код'),
            'brand_model': _('Марка и модель'),
            'color': _('Цвет кузова'),
            'vehicle_type': _('Тип кузова'),
            'category': _('Категория ТС'),
            'fuel_type': _('Тип топлива'),
            'body_type': _('Тип кузова (детальный)'),
            'photo': _('Фотография ТС'),
            'pts_type': _('Тип паспорта'),
            'pts_series': _('Серия ПТС'),
            'pts_number': _('Номер ПТС'),
            'pts_date': _('Дата выдачи ПТС'),
            'pts_scan': _('Скан ПТС'),
            'epts_number': _('Номер ЭПТС'),
            'epts_date': _('Дата выдачи ЭПТС'),
            'epts_scan': _('Скан ЭПТС'),

            # BLOCK 2
            'grz_series': _('Серия ГРЗ'),
            'grz_number': _('Номер ГРЗ'),
            'grz_date': _('Дата выдачи ГРЗ'),
            'reg_certificate_series': _('Серия свидетельства регистрации'),
            'reg_certificate_number': _('Номер свидетельства регистрации'),
            'reg_certificate_date': _('Дата выдачи свидетельства'),
            'reg_certificate_scan': _('Скан свидетельства регистрации'),
            'osago_number': _('Номер полиса ОСАГО'),
            'osago_date_issued': _('Дата выдачи ОСАГО'),
            'osago_date_expiry': _('Дата истечения ОСАГО'),
            'osago_cost': _('Стоимость полиса ОСАГО'),
            'osago_scan': _('Скан полиса ОСАГО'),
            'diagnostic_card_number': _('Номер диагностической карты'),
            'diagnostic_card_date': _('Дата диагностической карты'),
            'diagnostic_card_expiry': _('Дата истечения диагностической карты'),
            'diagnostic_card_scan': _('Скан диагностической карты'),

            # BLOCK 3
            'mass_kg': _('Масса (кг)'),
            'empty_mass': _('Масса без нагрузки (кг)'),
            'cargo_capacity': _('Грузоподъемность (кг)'),
            'engine_volume': _('Объём двигателя (л)'),
            'engine_power_hp': _('Мощность двигателя (л.с.)'),
            'engine_power_kw': _('Мощность двигателя (кВт)'),
            'engine_model_number': _('Модель, № двигателя'),
            'chassis_number': _('Номер шасси'),
            'body_number': _('Номер кузова'),
            'year_of_manufacture': _('Год изготовления'),
            'mileage_km': _('Пробег (км)'),
            'motor_hours': _('Моточасы для ДСМ (час.)'),
            'mileage_type': _('Тип пробега'),
            'passenger_capacity': _('Пассажировместимость (чел.)'),
            'bus_length': _('Габаритная длина автобуса (м)'),
            'bucket_capacity': _('Ёмкость ковша (м³)'),
            'fuel_tank_capacity': _('Ёмкость топливного бака (л)'),
            'fuel_grade': _('Марка ГСМ'),
            'fuel_consumption_type': _('Расходы ГСМ (тип единицы)'),
            'fuel_consumption_summer_city': _('Расходы ГСМ (Лето город)'),
            'fuel_consumption_summer_highway': _('Расходы ГСМ (Лето трасса)'),
            'fuel_consumption_winter_city': _('Расходы ГСМ (Зима город)'),
            'fuel_consumption_winter_highway': _('Расходы ГСМ (Зима трасса)'),
            'fuel_consumption_per_hour': _('Расходы ГСМ (литр/час)'),
            'gbo_present': _('Наличие ГБО'),
            'gbo_type': _('Тип ГБО'),
            'gbo_volume': _('Объём ГБО (л)'),
            'gbo_installation_date': _('Дата установки ГБО'),
            'gbo_cylinders_count': _('Количество баллонов ГБО (шт.)'),
            'gbo_total_capacity': _('Общая ёмкость баллонов ГБО (л)'),
            'gbo_inspection_date': _('Дата освидетельствования ГБО'),
            'gbo_next_inspection_date': _('Дата следующего освидетельствования ГБО'),
            'gbo_inspection_scan': _('Скан свидетельства ГБО'),
            'dprg_inspection_date': _('Дата осмотра в ГИБДД (ДПОГ)'),
            'dprg_next_inspection_date': _('Дата следующего осмотра в ГИБДД (ДПОГ)'),
            'dprg_inspection_scan': _('Скан ДПОГ'),
            'has_ssmt': _('Наличие ССМТ'),
            'has_tachograph': _('Наличие тахографа'),
            'tachograph_calibration_date': _('Дата калибровки тахографа'),
            'tachograph_next_calibration_date': _('Дата следующей калибровки тахографа'),
            'has_lifting_equipment': _('Наличие подъемного оборудования'),
            'initial_cost': _('Первоначальная стоимость'),
            'vehicle_type_for_military': _('Тип ТС (для военкомата)'),
            'vehicle_type_for_tax': _('Тип ТС (для налоговой)'),
            'inventory_number': _('Инвентарный номер ТС'),
            'motorpool': _('Автоколонна'),
            'direction': _('Направление ТС'),
            'ts_status': _('Статус ТС'),
            'dismission_date': _('Дата снятия с учета в ГИБДД'),
            'axles_count': _('Количество осей'),
            'to2_periodicity': _('Периодичность проведения ТО-2 (км)'),

            # BLOCK 4
            'to2_period_days': _('Период ТО-2 (дней)'),
            'to3_period_days': _('Период ТО-3 (дней)'),
            'tech_inspection_expiry': _('Дата истечения техосмотра'),
            'insurance_expiry': _('Дата истечения страховки'),
            'okof_code': _('Код ОКОФ'),
            'date_in_service': _('Дата ввода в эксплуатацию'),
            'depreciation_rate': _('Норма амортизации (%)'),
            'accumulated_depreciation': _('Накопленная амортизация (Р)'),
            'residual_value': _('Остаточная стоимость (Р)'),

            # ARCHIVE
            'is_archived': _('Архивировано'),
        }

        help_texts = {
            'garage_number': _('Уникальный номер ТС в учете цеха'),
            'vin': _('17-символьный идентификационный номер кузова'),
            'epts_number': _('Номер электронного паспорта'),
            'grz_series': _('Серия государственного номера'),
            'grz_number': _('Номер государственного регистрационного знака'),
            'fuel_grade': _('ДТ, АИ-92, АИ-95, ГАЗ, Электро и комбинации'),
            'engine_model_number': _('15+ символов'),
            'chassis_number': _('20+ символов'),
            'body_number': _('20+ символов'),
            'year_of_manufacture': _('ГГГГ'),
            'initial_cost': _('10+ символов'),
            'inventory_number': _('7+ символов'),
            'motorpool': _('01, 02, 03 и т.д.'),
            'direction': _('Дублирует первую цифру гаражного номера'),
            'okof_code': _('Общероссийский классификатор основных фондов'),
        }


class MaintenanceScheduleForm(forms.ModelForm):
    """Form for creating and editing TO-2 maintenance schedules."""

    class Meta:
        model = MaintenanceSchedule
        fields = [
            'vehicle', 'status',
            'last_maintenance_date', 'last_maintenance_mileage',
            'next_maintenance_date', 'next_maintenance_mileage',
            'notes'
        ]

        widgets = {
            'vehicle': forms.Select(attrs={
                'class': 'form-select'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'last_maintenance_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'last_maintenance_mileage': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'next_maintenance_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'next_maintenance_mileage': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Результаты ТО-2 или замечания'
            }),
        }

        labels = {
            'vehicle': _('Транспортное средство'),
            'status': _('Статус'),
            'last_maintenance_date': _('Дата последней ТО-2'),
            'last_maintenance_mileage': _('Пробег при последней ТО-2 (км)'),
            'next_maintenance_date': _('Дата следующей ТО-2'),
            'next_maintenance_mileage': _('Пробег для следующей ТО-2 (км)'),
            'notes': _('Заметки'),
        }
