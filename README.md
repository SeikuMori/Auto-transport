# ЭХП РОСАТОМ — Система управления автотранспортом

Это Django-приложение для управления парком автотранспорта компании РОСАТОМ. Система отслеживает транспортные средства, их техническое обслуживание, документы и сроки их действия.

## 📋 Содержание

- [Обзор](#обзор)
- [Функциональность](#функциональность)
- [Требования](#требования)
- [Установка и запуск](#установка-и-запуск)
- [Структура проекта](#структура-проекта)
- [Основные компоненты](#основные-компоненты)
- [Архитектура и дизайн](#архитектура-и-дизайн)
- [API и представления](#api-и-представления)
- [База данных](#база-данных)

---

## 🎯 Обзор

Система управления ЭХП (Автотранспортный цех 013) предоставляет веб-интерфейс для:

- Управления парком транспортных средств (ТС)
- Отслеживания документов ТС и сроков их действия
- Учёта технического обслуживания (ТО-2)
- Управления гаражными номерами
- Генерации отчётов и аудита
- Настройки параметров приложения

**Ключевая особенность**: Система автоматически выделяет красным/жёлтым цветом ТС с истекшими или истекающими в течение 30 дней документами.

---

## ✨ Функциональность

### 1. Управление транспортными средствами
- Списки ТС с поиском, фильтрацией и пагинацией
- Создание, редактирование, удаление ТС
- Детальная информация по каждому ТС
- Отслеживание статуса документов

### 2. Система отслеживания документов (6 типов)
- ОСАГО (страховой полис)
- Техническое обслуживание (техосмотр)
- Диагностическая карта
- ГБО (газобаллонное оборудование) — проверки
- ДПОГ — проверки
- Тахограф — калибровка

**Визуальное отслеживание:**
- 🔴 Красное выделение — документ истек
- 🟡 Жёлтое выделение — документ истекает в течение 30 дней
- ✅ Нормальное отображение — документ в порядке

### 3. Техническое обслуживание (ТО-2)
- Графики прохождения ТО
- Отслеживание планов и фактических дат
- Интеграция с календарём ТО

### 4. Навигация (5 разделов в navbar)
1. **Система** — настройки, справка, выход
2. **Справочники** — ТС, архив, справочники
3. **Сервис** — свободные гаражные номера
4. **Тех.обслуживание** — ТО-2, графики
5. **Отчёты** — аудит, экспорт, таблицы

### 5. Дополнительные возможности
- Журнал аудита (все действия пользователей)
- Экспорт данных в Excel
- Система прав доступа (группы пользователей)
- Аутентификация и авторизация
- Кеширование данных для оптимизации

---

## 📦 Требования

- **Python** 3.10+
- **Django** 4.2 / 5.x
- **PostgreSQL** (рекомендуется) или SQLite
- **Bootstrap** 5
- **Font Awesome** 6.5.0 (иконки)

### Дополнительные пакеты

```
django>=4.2
psycopg2-binary>=2.9.0  # Драйвер PostgreSQL
openpyxl>=3.10.0       # Excel экспорт
Pillow>=9.0.0          # Обработка изображений
```

Полный список см. в `requirements.txt`.

---

## 🚀 Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/SeikuMori/Auto-transport.git
cd Auto-transport
```

### 2. Виртуальное окружение

```powershell
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Конфигурация БД

Отредактируйте `personal_card_system/settings.py` (раздел `DATABASES`):

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'auto_transport_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Или используйте переменные окружения (см. `.env.example`).

### 5. Миграции БД

```bash
python manage.py migrate
```

### 6. Создание суперпользователя

```bash
python manage.py createsuperuser
```

### 7. Запуск сервера разработки

```bash
python manage.py runserver
```

Откройте в браузере: **http://127.0.0.1:8000/**

---

## 📁 Структура проекта

```
Auto-transport/
├── personal_card_system/    # Django проект (settings, urls, wsgi)
│   ├── settings.py         # Основные настройки
│   ├── urls.py             # Главные маршруты
│   └── wsgi.py / asgi.py   # WSGI/ASGI конфигурация
│
├── cards/                  # Django приложение (основная логика)
│   ├── models.py          # Модели (Vehicle, Document, Maintenance и т.д.)
│   ├── views.py           # Представления (ListView, DetailView и т.д.)
│   ├── urls.py            # Маршруты приложения
│   ├── admin.py           # Админка Django
│   ├── forms.py           # Формы (если используются)
│   ├── migrations/        # Миграции БД
│   ├── locale/            # Файлы локализации (ru, en и т.д.)
│   └── templates/cards/   # Шаблоны приложения
│
├── templates/             # Глобальные шаблоны
│   ├── base.html         # Базовый шаблон с navbar
│   ├── includes/         # Переиспользуемые компоненты
│   │   └── navbar.html  # Навигационная полоса (5 разделов)
│   └── cards/            # Шаблоны для приложения cards
│       ├── vehicle_list.html        # Список ТС
│       ├── vehicle_detail.html      # Детали ТС
│       ├── settings.html            # Настройки приложения
│       ├── about.html               # Справочная информация
│       ├── free_garage_numbers.html # Свободные номера гаражей
│       ├── maintenance_base.html    # ТО (техническое обслуживание)
│       └── reports_base.html        # Отчёты
│
├── static/                # Статические файлы
│   ├── css/
│   │   └── style.css     # Стили приложения (gradient, navbar, highlighting)
│   ├── js/               # JavaScript файлы
│   └── images/           # Логотипы и изображения
│
├── media/                 # Загружаемые файлы (фото ТС и т.д.)
│
├── manage.py             # Утилиты Django
├── requirements.txt      # Зависимости проекта
└── README.md            # Этот файл
```

---

## 🔧 Основные компоненты

### 1. Модель Vehicle (cards/models.py)

Основная модель приложения с полями:
- `make` — Марка (Газель, Волга и т.д.)
- `model` — Модель
- `registration_number` — Регистрационный номер (ГОС номер)
- `vin_number` — VIN номер
- `garage_number` — Номер гаража (1-10000)
- `photo` — Фото ТС
- Документы: ОСАГО, техосмотр, диагностическая карта, ГБО, ДПОГ, тахограф
- Даты истечения документов

**Ключевые методы:**
```python
get_expiring_documents(days_threshold=30)  # Возвращает истекшие/истекающие документы
get_expiry_class()                         # CSS класс для подсветки (row-expired, row-expiring)
get_expiry_status()                        # Статус документов (danger, warning, success)
```

### 2. Представления (views.py)

- `VehicleListView` — список ТС с фильтрацией
- `VehicleDetailView` — детали ТС
- `VehicleCreateView` — создание ТС
- `VehicleUpdateView` — редактирование ТС
- `VehicleDeleteView` — удаление ТС
- `SettingsView` — настройки приложения
- `AboutView` — справочная информация
- `FreeGarageNumbersView` — свободные номера гаражей
- `MaintenanceBaseView` — главная страница ТО
- `ReportsBaseView` — главная страница отчётов

Все представления используют `LoginRequiredMixin` для защиты.

### 3. Маршруты (urls.py)

```python
path('vehicles/', VehicleListView.as_view(), name='vehicle_list')
path('vehicles/<int:pk>/', VehicleDetailView.as_view(), name='vehicle_detail')
path('vehicles/add/', VehicleCreateView.as_view(), name='vehicle_add')
path('vehicles/<int:pk>/edit/', VehicleUpdateView.as_view(), name='vehicle_edit')
path('vehicles/<int:pk>/delete/', VehicleDeleteView.as_view(), name='vehicle_delete')

path('settings/', SettingsView.as_view(), name='settings')
path('about/', AboutView.as_view(), name='about')
path('free-garage-numbers/', FreeGarageNumbersView.as_view(), name='free_garage_numbers')
path('maintenance/', MaintenanceBaseView.as_view(), name='maintenance_base')
path('reports/', ReportsBaseView.as_view(), name='reports_base')
```

---

## 🎨 Архитектура и дизайн

### Навигационная система (5 разделов)

**navbar.html** структурирована следующим образом:

```
┌─────────────────────────────────────────────────────────────┐
│ 🚚 ЭХП РОСАТОМ  │ Система ▼ │ Справочники ▼ │ Сервис ▼ │ ТО ▼ │ Отчёты ▼ │  👤 Профиль
└─────────────────────────────────────────────────────────────┘
```

### CSS стилизация (static/css/style.css)

- **Фон**: Gradient background (light blue to gray)
- **Navbar**: Dark theme с синей линией 3px
- **Логотип**:
  - 🚚 Иконка грузовика (Font Awesome `fas fa-truck`)
  - Hover эффект: масштабирование (1.05) + свечение текста
  - Иконка вращается на 5°
- **Выделение документов**:
  - `.row-expired` — красный фон (rgba(220, 53, 69, 0.15))
  - `.row-expiring` — жёлтый фон (rgba(255, 193, 7, 0.15))
  - Левая граница (4px) для визуального акцента
- **Иконки**: Color-coded icons (green — OK, yellow — warning, red — expired)

### Responsive дизайн

- Все компоненты используют Bootstrap 5
- Navbar сворачивается на мобильных (burger menu)
- Таблицы responsive (горизонтальная прокрутка на мобильных)

---

## 📊 API и представления

### Документы и статусы

Система отслеживает 6 типов документов для каждого ТС:

| Документ | Поле модели | Статус |
|----------|-------------|--------|
| ОСАГО | `osago_date_expiry` | Обязателен |
| Техосмотр | `tech_inspection_expiry` | Обязателен |
| Диагностическая карта | `diagnostic_card_expiry` | Обязателен |
| ГБО проверка | `gbo_next_inspection_date` | Если установлено ГБО |
| ДПОГ проверка | `dprg_next_inspection_date` | Если установлено ДПОГ |
| Тахограф калибровка | `tachograph_next_calibration_date` | Обязателен |

### Status Codes

- `danger` — документ истёк (дата < сегодня)
- `warning` — документ истекает (дата ≤ сегодня + 30 дней)
- `success` — документ в порядке (дата > сегодня + 30 дней)
- `info` — документ не заполнен (null)

---

## 🗄️ База данных

### Модели

**Vehicle** (основная модель):
```python
class Vehicle(models.Model):
    make                            # Марка
    model                           # Модель
    registration_number             # ГОС номер
    vin_number                      # VIN
    garage_number                   # 1-10000
    photo                           # Фото ТС

    # Документы (DateField)
    osago_date_expiry               # ОСАГО
    tech_inspection_expiry          # Техосмотр
    diagnostic_card_expiry          # Диагностическая карта
    gbo_next_inspection_date        # ГБО
    dprg_next_inspection_date       # ДПОГ
    tachograph_next_calibration_date # Тахограф

    # Служебные поля
    created_at                      # Дата создания
    updated_at                      # Дата обновления
    archived                        # Архивировано (bollean)
```

### Миграции

Все миграции находятся в `cards/migrations/`. Для синхронизации БД используйте:

```bash
python manage.py migrate
```

### Резервная копия БД

```bash
# PostgreSQL
pg_dump auto_transport_db > backup.sql

# Восстановление
psql auto_transport_db < backup.sql
```

---

## 🔐 Безопасность

- ✅ Все представления требуют аутентификации (`LoginRequiredMixin`)
- ✅ CSRF защита включена
- ✅ SQL-инъекции предотвращены (использование ORM)
- ✅ Проверка прав доступа на основе групп пользователей
- ⚠️ SECRET_KEY должен быть защищен в production (используйте .env файл)

### Рекомендации для продакшна

1. Установите `DEBUG = False` в settings.py
2. Настройте `ALLOWED_HOSTS`
3. Используйте `https://` и HSTS headers
4. Установите `SESSION_COOKIE_SECURE = True`
5. Используйте переменные окружения для конфиденциальных данных
6. Регулярно обновляйте зависимости (`pip install --upgrade`)

---

## 📝 Лицензия и контакты

Проект для дипломной работы ЭХП РОСАТОМ, Автотранспортный цех 013.

**GitHub**: https://github.com/SeikuMori/Auto-transport

---

## 🛠️ Полезные команды

```bash
# Создание миграций после изменения моделей
python manage.py makemigrations

# Применение миграций
python manage.py migrate

# Запуск shell для интерактивного Python
python manage.py shell

# Сбор статических файлов (для production)
python manage.py collectstatic

# Запуск тестов
python manage.py test

# Проверка кода на ошибки
python manage.py check

# Создание суперпользователя
python manage.py createsuperuser
```

---

## 📈 Дальнейшее развитие

Планируемые улучшения:
- [ ] Интеграция с email-уведомлениями об истечении документов
- [ ] SMS-уведомления
- [ ] Мобильное приложение (React Native / Flutter)
- [ ] REST API (Django REST Framework)
- [ ] Расширенная аналитика по парку ТС
- [ ] Интеграция с системой GPS-мониторинга
- [ ] Система оценки расходов на ТО

---

**Спасибо за использование ЭХП Management System!** 🚀
