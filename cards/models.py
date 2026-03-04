from django.db import models
from django.contrib.auth.models import User


# ===== ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ =====

class UserProfile(models.Model):
    """
    Расширение модели User для хранения дополнительных данных сотрудников.

    Связь OneToOne с User:
    - fio: полное имя (ФИО)
    - tab_number: табельный номер
    - position: должность
    """
    POSITION_CHOICES = (
        ('admin', 'Администратор'),
        ('supervisor', 'Руководитель'),
        ('specialist', 'Специалист'),
        ('user', 'Пользователь'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name="Пользователь"
    )

    fio = models.CharField(
        max_length=255,
        verbose_name="ФИО",
        help_text="Полное имя сотрудника"
    )

    tab_number = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="Табельный номер",
        help_text="Уникальный табельный номер"
    )

    position = models.CharField(
        max_length=50,
        verbose_name="Должность",
        help_text="Должность сотрудника"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    def __str__(self):
        return f"{self.fio} ({self.user.username})"

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"
        ordering = ['fio']


# ===== СПРАВОЧНЫЕ МОДЕЛИ =====

class BrandModel(models.Model):
    """
    Справочник марок и моделей транспортных средств.

    Примеры: ГАЗ 3309, КАМАЗ 5320, МАЗ 5551 и т.д.
    """
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Марка и модель"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Марка и модель"
        verbose_name_plural = "Марки и модели"
        ordering = ['name']


class Color(models.Model):
    """
    Справочник цветов кузова транспортных средств.

    Примеры: Белый, Красный, Чёрный, Синий и т.д.
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Цвет"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Цвет кузова"
        verbose_name_plural = "Цвета кузова"
        ordering = ['name']


class VehicleType(models.Model):
    """
    Справочник типов кузова транспортных средств.

    Примеры: Грузовик, Самосвал, Фургон, Цистерна и т.д.
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Тип кузова"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип кузова"
        verbose_name_plural = "Типы кузова"
        ordering = ['name']


class Category(models.Model):
    """
    Справочник категорий транспортных средств.

    Примеры: Легковой, Грузовой, Автобус, Специальная техника и т.д.
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Категория ТС"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория ТС"
        verbose_name_plural = "Категории ТС"
        ordering = ['name']


class FuelType(models.Model):
    """
    Справочник типов топлива (двигателя).

    Примеры: Бензин, Дизель, СНГ (газоснабжение), Электро и т.д.
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Тип топлива"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип топлива"
        verbose_name_plural = "Типы топлива"
        ordering = ['name']


class BodyType(models.Model):
    """
    Справочник типов кузова (детализированный).

    Примеры: Седан, Универсал, Купе, Хэтчбек, Минивэн и т.д.
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Тип кузова (детальный)"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип кузова (детальный)"
        verbose_name_plural = "Типы кузова (детальные)"
        ordering = ['name']


# ===== ОСНОВНАЯ МОДЕЛЬ =====

class Vehicle(models.Model):
    """
    Модель `Vehicle` соответствует записи (карточке) транспортного средства.

    Блок 1: Паспорт транспортного средства (ПТС/ЭПТС, VIN, марка, модель и т.д.)
    - garage_number: гаражный номер (уникальный идентификатор ТС в учете)
    - vin: VIN номер кузова (17 символов)
    - brand_model: марка и модель (CharField пока, станет ForeignKey в задаче 2)
    - photo: фотография ТС
    - pts_type: тип паспорта (ПТС или ЭПТС) - choices
    - pts_series/number/date: реквизиты бумажного ПТС
    - epts_number/date: реквизиты электронного ПТС (ЭПТС)
    - pts_scan, epts_scan: сканы документов

    Методы и поведение:
    - __str__: удобное строковое представление (гаражный номер + марка)
    - Meta: читаемые имена модели и порядок по умолчанию
    """

    PTS_TYPE_CHOICES = (
        ('pts', 'ПТС (бумажный паспорт)'),
        ('epts', 'ЭПТС (электронный паспорт)'),
    )

    VEHICLE_TYPE_MILITARY_CHOICES = (
        ('passenger', 'Легковой'),
        ('truck', 'Грузовой'),
        ('bus', 'Автобус'),
        ('flat_bed', 'Бортовой'),
        ('dump', 'Самосвал'),
        ('other', 'Прочее'),
    )

    VEHICLE_TYPE_TAX_CHOICES = (
        ('passenger', 'Легковой'),
        ('truck', 'Грузовой'),
        ('bus', 'Автобус'),
        ('flat_bed', 'Бортовой'),
        ('dump', 'Самосвал'),
        ('other', 'Прочее'),
    )

    FUEL_CONSUMPTION_TYPE_CHOICES = (
        ('liters_100km', 'литр / 100 км'),
        ('liters_hour', 'литр / час'),
        ('cubic_100km', 'м³ / 100 км'),
        ('hybrid', 'гибрид'),
        ('other', 'прочее'),
    )

    MILEAGE_TYPE_CHOICES = (
        ('km', 'Пробег для ТС (км)'),
        ('hours', 'Моточасы для ДСМ (час.)'),
    )


    # === БЛОК 1: ПАСПОРТ ТРАНСПОРТНОГО СРЕДСТВА ===
    garage_number = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Гаражный номер",
        help_text="Уникальный номер ТС в учете цеха"
    )

    vin = models.CharField(
        max_length=17,
        verbose_name="VIN номер",
        help_text="17-символьный идентификационный номер кузова"
    )

    brand_model = models.ForeignKey(
        BrandModel,
        on_delete=models.PROTECT,
        verbose_name="Марка и модель",
        blank=True,
        null=True,
        help_text="Выберите из справочника или создайте новую"
    )

    # Новые справочники из задачи 2
    color = models.ForeignKey(
        Color,
        on_delete=models.SET_NULL,
        verbose_name="Цвет кузова",
        blank=True,
        null=True
    )

    vehicle_type = models.ForeignKey(
        VehicleType,
        on_delete=models.SET_NULL,
        verbose_name="Тип кузова",
        blank=True,
        null=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="Категория ТС",
        blank=True,
        null=True
    )

    fuel_type = models.ForeignKey(
        FuelType,
        on_delete=models.SET_NULL,
        verbose_name="Тип топлива",
        blank=True,
        null=True
    )

    body_type = models.ForeignKey(
        BodyType,
        on_delete=models.SET_NULL,
        verbose_name="Тип кузова (детальный)",
        blank=True,
        null=True
    )

    photo = models.ImageField(
        upload_to='vehicles/',
        blank=True,
        null=True,
        verbose_name="Фотография ТС"
    )

    # Паспорт (ПТС/ЭПТС) - выбор типа
    pts_type = models.CharField(
        max_length=10,
        choices=PTS_TYPE_CHOICES,
        default='pts',
        verbose_name="Тип паспорта"
    )

    # Реквизиты бумажного ПТС
    pts_series = models.CharField(
        max_length=4,
        blank=True,
        verbose_name="Серия ПТС",
        help_text="Например: 78 РС"
    )

    pts_number = models.CharField(
        max_length=6,
        blank=True,
        verbose_name="Номер ПТС",
        help_text="6 цифр"
    )

    pts_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата выдачи ПТС"
    )

    pts_scan = models.FileField(
        upload_to='vehicles/pts/',
        blank=True,
        null=True,
        verbose_name="Скан ПТС"
    )

    # Реквизиты электронного ПТС (ЭПТС)
    epts_number = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Номер ЭПТС",
        help_text="Номер электронного паспорта"
    )

    epts_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата выдачи ЭПТС"
    )

    epts_scan = models.FileField(
        upload_to='vehicles/epts/',
        blank=True,
        null=True,
        verbose_name="Скан ЭПТС"
    )

    # === БЛОК 2: РЕГИСТРАЦИОННЫЕ ДАННЫЕ ГИБДД ===
    # Государственный регистрационный номер (ГРЗ)
    grz_series = models.CharField(
        max_length=2,
        blank=True,
        verbose_name="Серия ГРЗ",
        help_text="Например: 78"
    )

    grz_number = models.CharField(
        max_length=6,
        blank=True,
        verbose_name="Номер ГРЗ",
        help_text="Например: АА123БВ"
    )

    grz_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата выдачи ГРЗ"
    )

    # Свидетельство о регистрации ТС
    reg_certificate_series = models.CharField(
        max_length=4,
        blank=True,
        verbose_name="Серия свидетельства регистрации"
    )

    reg_certificate_number = models.CharField(
        max_length=6,
        blank=True,
        verbose_name="Номер свидетельства регистрации"
    )

    reg_certificate_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата выдачи свидетельства"
    )

    reg_certificate_scan = models.FileField(
        upload_to='vehicles/registration/',
        blank=True,
        null=True,
        verbose_name="Скан свидетельства регистрации"
    )

    # ОСАГО (обязательное страхование)
    osago_number = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Номер полиса ОСАГО"
    )

    osago_date_issued = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата выдачи ОСАГО"
    )

    osago_date_expiry = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата истечения ОСАГО"
    )

    osago_scan = models.FileField(
        upload_to='vehicles/osago/',
        blank=True,
        null=True,
        verbose_name="Скан полиса ОСАГО"
    )

    # Диагностическая карта
    diagnostic_card_number = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Номер диагностической карты"
    )

    diagnostic_card_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата диагностической карты"
    )

    diagnostic_card_expiry = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата истечения диагностической карты"
    )

    diagnostic_card_scan = models.FileField(
        upload_to='vehicles/diagnostic/',
        blank=True,
        null=True,
        verbose_name="Скан диагностической карты"
    )

    # === БЛОК 3: ОБЩИЕ ХАРАКТЕРИСТИКИ ===
    mass_kg = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Масса (кг)"
    )

    mileage_km = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Пробег (км)"
    )

    engine_volume = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Объём двигателя (л)"
    )

    engine_power_hp = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Мощность двигателя (л.с.)"
    )

    engine_power_kw = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Мощность двигателя (кВт)"
    )

    engine_model_number = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Модель, № двигателя",
        help_text="15+ символов"
    )

    chassis_number = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Номер шасси",
        help_text="20+ символов"
    )

    body_number = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Номер кузова",
        help_text="20+ символов"
    )

    year_of_manufacture = models.CharField(
        max_length=4,
        blank=True,
        verbose_name="Год изготовления",
        help_text="ГГГГ"
    )

    empty_mass = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Масса без нагрузки (кг)"
    )

    cargo_capacity = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Грузоподъемность (кг)"
    )

    passenger_capacity = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Пассажировместимость (чел.)"
    )

    bus_length = models.DecimalField(
        max_digits=6,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name="Габаритная длина автобуса (м)"
    )

    bucket_capacity = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name="Ёмкость ковша (м³)"
    )

    fuel_tank_capacity = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name="Ёмкость топливного бака (л)"
    )

    fuel_grade = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Марка ГСМ",
        help_text="ДТ, АИ-92, АИ-95, ГАЗ, Электро и комбинации"
    )

    initial_cost = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Первоначальная стоимость",
        help_text="10+ символов"
    )

    vehicle_type_for_military = models.CharField(
        max_length=20,
        choices=VEHICLE_TYPE_MILITARY_CHOICES,
        blank=True,
        verbose_name="Тип ТС (для военкомата)"
    )

    vehicle_type_for_tax = models.CharField(
        max_length=20,
        choices=VEHICLE_TYPE_TAX_CHOICES,
        blank=True,
        verbose_name="Тип ТС (для налоговой)"
    )

    dismission_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата снятия с учета в ГИБДД"
    )

    osago_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Стоимость полиса ОСАГО (Р)"
    )

    axles_count = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Количество осей"
    )

    # === БЛОК 3 (продолжение): ОБЩИЕ (ПРОЧИЕ) СВЕДЕНИЯ ===
    inventory_number = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Инвентарный номер ТС",
        help_text="7+ символов"
    )

    motorpool = models.CharField(
        max_length=10,
        blank=True,
        verbose_name="Автоколонна",
        help_text="01, 02, 03 и т.д."
    )

    direction = models.CharField(
        max_length=1,
        blank=True,
        verbose_name="Направление ТС",
        help_text="Дублирует первую цифру гаражного номера"
    )

    fuel_consumption_type = models.CharField(
        max_length=20,
        choices=FUEL_CONSUMPTION_TYPE_CHOICES,
        blank=True,
        verbose_name="Расходы ГСМ (тип единицы)"
    )

    fuel_consumption_summer_city = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Расходы ГСМ (Лето город)"
    )

    fuel_consumption_summer_highway = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Расходы ГСМ (Лето трасса)"
    )

    fuel_consumption_winter_city = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Расходы ГСМ (Зима город)"
    )

    fuel_consumption_winter_highway = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Расходы ГСМ (Зима трасса)"
    )

    fuel_consumption_per_hour = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Расходы ГСМ (литр/час)"
    )

    gbo_cylinders_count = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Количество баллонов ГБО (шт.)"
    )

    gbo_total_capacity = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name="Общая ёмкость баллонов ГБО (л)"
    )

    gbo_inspection_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата освидетельствования ГБО"
    )

    gbo_next_inspection_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата следующего освидетельствования ГБО"
    )

    gbo_inspection_scan = models.FileField(
        upload_to='vehicles/gbo/',
        blank=True,
        null=True,
        verbose_name="Скан свидетельства ГБО"
    )

    dprg_inspection_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата осмотра в ГИБДД (ДПОГ)"
    )

    dprg_next_inspection_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата следующего осмотра в ГИБДД (ДПОГ)"
    )

    dprg_inspection_scan = models.FileField(
        upload_to='vehicles/dprg/',
        blank=True,
        null=True,
        verbose_name="Скан ДПОГ"
    )

    has_ssmt = models.BooleanField(
        default=False,
        verbose_name="Наличие ССМТ"
    )

    has_tachograph = models.BooleanField(
        default=False,
        verbose_name="Наличие тахографа"
    )

    tachograph_calibration_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата калибровки тахографа"
    )

    tachograph_next_calibration_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата следующей калибровки тахографа"
    )

    has_lifting_equipment = models.BooleanField(
        default=False,
        verbose_name="Наличие подъемного оборудования"
    )

    mileage_type = models.CharField(
        max_length=10,
        choices=MILEAGE_TYPE_CHOICES,
        default='km',
        blank=True,
        verbose_name="Тип пробега"
    )

    motor_hours = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Моточасы для ДСМ (час.)"
    )

    to2_periodicity = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Периодичность проведения ТО-2 (км)"
    )

    ts_status = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Статус ТС",
        help_text="в рейсе, ремонт, ТО-1, ТО-2, дежурство, простой"
    )

    gbo_present = models.BooleanField(
        default=False,
        verbose_name="Наличие ГБО"
    )

    gbo_type = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Тип ГБО",
        help_text="Например: ГБО-4, СНГ и т.д."
    )

    gbo_volume = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Объём ГБО (л)"
    )

    gbo_installation_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата установки ГБО"
    )

    # === БЛОК 4: ДОКУМЕНТЫ ПО СРОКАМ ===
    to2_period_days = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Период ТО-2 (дней)"
    )

    to3_period_days = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Период ТО-3 (дней)"
    )

    tech_inspection_expiry = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата истечения техосмотра"
    )

    insurance_expiry = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата истечения страховки"
    )

    # === БЛОК 5: БУХГАЛТЕРСКИЕ ДАННЫЕ ===
    okof_code = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Код ОКОФ",
        help_text="Общероссийский классификатор основных фондов (например: 1700000000194)"
    )

    date_in_service = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата ввода в эксплуатацию",
        help_text="Для расчета износа и амортизации"
    )

    depreciation_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Норма амортизации (%)",
        help_text="Годовой процент амортизации"
    )

    accumulated_depreciation = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Накопленная амортизация (Р)"
    )

    residual_value = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Остаточная стоимость (Р)"
    )

    # === АРХИВИРОВАНИЕ ===
    is_archived = models.BooleanField(
        default=False,
        verbose_name="Архивировано",
        db_index=True,
        help_text="Снято с учета / выведено из эксплуатации"
    )

    archived_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Дата архивирования"
    )

    archived_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='archived_vehicles',
        verbose_name="Архивировано пользователем"
    )

    def get_expiring_documents(self, days_threshold=30):
        """
        Получить список документов, которые истекают в течение N дней.
        Проверяет все 6 документов: ОСАГО, техосмотр, диагностическая карта,
        проверка ГБО, проверка ДПОГ и калибровка тахографа.

        Args:
            days_threshold: количество дней для нежелательных сроков (по умолчанию 30)

        Returns:
            dict с ключами: 'expired', 'expiring', 'ok', 'warnings' (отсортирован по приоритету)
        """
        from datetime import date, timedelta

        result = {
            'expired': [],        # Истекло (КРИТИЧНО - красный)
            'expiring': [],       # Истекает в течение N дней (ВНИМАНИЕ - жёлтый)
            'ok': [],            # В норме (зелёный)
            'warnings': [],      # Предупреждения (пусто значение - серый)
        }

        today = date.today()
        threshold_date = today + timedelta(days=days_threshold)

        # Список документов и их полей для проверки
        documents = [
            (self.osago_date_expiry, 'Полис ОСАГО'),
            (self.tech_inspection_expiry, 'Техосмотр'),
            (self.diagnostic_card_expiry, 'Диагностическая карта'),
            (self.gbo_next_inspection_date, 'Проверка ГБО'),
            (self.dprg_next_inspection_date, 'Проверка ДПОГ'),
            (self.tachograph_next_calibration_date, 'Калибровка тахографа'),
        ]

        # Проверяем каждый документ
        for doc_date, doc_name in documents:
            if doc_date:
                if doc_date < today:
                    # ИСТЕКЛО - красный (danger)
                    result['expired'].append({
                        'name': doc_name,
                        'date': doc_date,
                        'days_left': (doc_date - today).days
                    })
                elif doc_date <= threshold_date:
                    # ИСТЕКАЕТ в течение N дней - жёлтый (warning)
                    result['expiring'].append({
                        'name': doc_name,
                        'date': doc_date,
                        'days_left': (doc_date - today).days
                    })
                else:
                    # ОК - зелёный (success)
                    result['ok'].append({
                        'name': doc_name,
                        'date': doc_date
                    })
            else:
                # НЕ УКАЗАНО - серый (info)
                result['warnings'].append({
                    'name': f'{doc_name} не указана'
                })

        return result

    def has_expiring_documents(self, days_threshold=30):
        """Проверить, есть ли документы в течение истечения"""
        expiring = self.get_expiring_documents(days_threshold)
        return len(expiring['expiring']) > 0 or len(expiring['expired']) > 0

    def get_expiry_status(self, days_threshold=30):
        """
        Получить общий статус документов.

        Returns:
            tuple (status, message)
            status: 'danger' (истекло), 'warning' (истекает), 'info' (не указано), 'success' (в норме)
        """
        expiring = self.get_expiring_documents(days_threshold)

        if expiring['expired']:
            return 'danger', f"ИСТЕКЛО: {len(expiring['expired'])} документов"
        elif expiring['expiring']:
            return 'warning', f"ВНИМАНИЕ: {len(expiring['expiring'])} документов истекает"
        elif expiring['warnings']:
            return 'info', f"Не заполнено: {len(expiring['warnings'])} полей"
        else:
            return 'success', "Все документы в норме"

    def get_days_until_expiry(self):
        """
        Получить минимальное количество дней до истечения любого документа.
        Проверяет все 6 документов, не только основные 3.

        Returns:
            int: дни до ближайшего истечения, или None если все заполнено и сроки нормальны
        """
        from datetime import date

        # Все поля дат для проверки (6 документов)
        date_fields = [
            self.osago_date_expiry,
            self.tech_inspection_expiry,
            self.diagnostic_card_expiry,
            self.gbo_next_inspection_date,
            self.dprg_next_inspection_date,
            self.tachograph_next_calibration_date,
        ]

        # Фильтруем заполненные даты
        filled_dates = [d for d in date_fields if d is not None]

        if not filled_dates:
            return None

        today = date.today()
        # Вычисляем дни до истечения для каждой даты
        days_list = [(d - today).days for d in filled_dates]

        # Возвращаем наименьшее значение (ближайшую дату)
        return min(days_list) if days_list else None

    def get_expiry_class(self, days_threshold=30):
        """
        Получить CSS класс для подсвечивания строки таблицы.
        Используется в шаблонах для класса-based highlighting вместо inline styles.

        Args:
            days_threshold: количество дней для определения "warning" статуса (по умолчанию 30)

        Returns:
            str: 'row-expired' (красно), 'row-expiring' (жёлтый), или '' (белый/нормальный)
        """
        expiring = self.get_expiring_documents(days_threshold)

        if expiring['expired']:
            return 'row-expired'  # Красное выделение
        elif expiring['expiring']:
            return 'row-expiring'  # Жёлтое выделение
        else:
            return ''  # Нет специального выделения

    def __str__(self):
        # Строковое представление: гаражный номер + марка/модель
        brand_name = self.brand_model.name if self.brand_model else "—"
        return f"[{self.garage_number}] {brand_name}"

    class Meta:
        # Читаемые имена и сортировка по умолчанию
        verbose_name = "Транспортное средство"
        verbose_name_plural = "Транспортные средства"
        ordering = ['garage_number']


# ===== ТЕХНИЧЕСКОЕ ОБСЛУЖИВАНИЕ (ТО-2) =====

class MaintenanceSchedule(models.Model):
    """
    Модель для управления расписанием техническое обслуживание ТО-2.

    Отслеживает:
    - Когда была последняя ТО-2
    - Когда следующая ТО-2 должна быть выполнена
    - Статус выполнения
    - Заметки и результаты
    """

    STATUS_CHOICES = (
        ('scheduled', 'Запланировано'),
        ('in_progress', 'В процессе'),
        ('completed', 'Завершено'),
        ('overdue', 'Просрочено'),
        ('cancelled', 'Отменено'),
    )

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='maintenance_schedules',
        verbose_name="Транспортное средство"
    )

    last_maintenance_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата последней ТО-2"
    )

    last_maintenance_mileage = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Пробег при последней ТО-2 (км)"
    )

    next_maintenance_date = models.DateField(
        verbose_name="Дата следующей ТО-2",
        db_index=True
    )

    next_maintenance_mileage = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Пробег для следующей ТО-2 (км)"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='scheduled',
        verbose_name="Статус",
        db_index=True
    )

    notes = models.TextField(
        blank=True,
        verbose_name="Заметки",
        help_text="Результаты ТО-2 или замечания"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    def __str__(self):
        return f"ТО-2 {self.vehicle.garage_number} - {self.get_status_display()}"

    class Meta:
        verbose_name = "Расписание ТО-2"
        verbose_name_plural = "Расписания ТО-2"
        ordering = ['next_maintenance_date']
        indexes = [
            models.Index(fields=['vehicle', '-next_maintenance_date']),
            models.Index(fields=['status', 'next_maintenance_date']),
        ]


# ===== АУДИТ-ЛОГИРОВАНИЕ =====

class AuditLog(models.Model):
    """
    Модель для логирования всех действий пользователя с транспортными средствами.

    Записывает:
    - user_fio: ФИО пользователя (из UserProfile)
    - username: логин пользователя (из User)
    - action: тип действия (CREATE, UPDATE, DELETE, VIEW)
    - model_name: название модели (обычно 'Vehicle')
    - object_id: ID объекта
    - object_description: описание объекта (например, гаражный номер и марка)
    - timestamp: дата и время действия
    - changes: описание внесённых изменений (для UPDATE)
    """
    ACTION_CHOICES = (
        ('CREATE', 'Создание'),
        ('UPDATE', 'Изменение'),
        ('DELETE', 'Удаление'),
        ('VIEW', 'Просмотр'),
    )

    user_fio = models.CharField(
        max_length=255,
        verbose_name="ФИО пользователя",
        db_index=True
    )

    username = models.CharField(
        max_length=150,
        verbose_name="Логин пользователя",
        db_index=True
    )

    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES,
        verbose_name="Действие",
        db_index=True
    )

    model_name = models.CharField(
        max_length=100,
        verbose_name="Модель",
        db_index=True
    )

    object_id = models.IntegerField(
        verbose_name="ID объекта",
        db_index=True
    )

    object_description = models.CharField(
        max_length=500,
        verbose_name="Описание объекта"
    )

    changes = models.TextField(
        blank=True,
        verbose_name="Внесённые изменения",
        help_text="Описание полей которые были изменены"
    )

    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата и время",
        db_index=True
    )

    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True,
        verbose_name="IP адрес"
    )

    def __str__(self):
        return f"{self.user_fio} - {self.get_action_display()} - {self.object_description} ({self.timestamp.strftime('%d.%m.%Y %H:%M:%S')})"

    class Meta:
        verbose_name = "Запись аудита"
        verbose_name_plural = "Записи аудита"
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['user_fio', '-timestamp']),
            models.Index(fields=['action', '-timestamp']),
        ]

# Конец файла models.py
