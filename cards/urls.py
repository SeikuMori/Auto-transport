from django.urls import path
from . import views

# Пространство имён приложения — позволяет ссылаться на URL'ы как 'cards:vehicle_list'
app_name = 'cards'

# Основной набор маршрутов для CRUD операций с моделью Vehicle
urlpatterns = [
    # Список всех транспортных средств
    path('', views.VehicleListView.as_view(), name='vehicle_list'),
    # Создать новое ТС
    path('add/', views.VehicleCreateView.as_view(), name='vehicle_add'),
    # Просмотреть детали ТС по PK
    path('<int:pk>/', views.VehicleDetailView.as_view(), name='vehicle_detail'),
    # Редактировать существующую запись
    path('<int:pk>/edit/', views.VehicleUpdateView.as_view(), name='vehicle_edit'),
    # Удалить запись (DeleteView ожидает POST из шаблона)
    path('<int:pk>/delete/', views.VehicleDeleteView.as_view(), name='vehicle_delete'),
    # Экспортировать в Excel
    path('export/', views.VehicleExportView.as_view(), name='vehicle_export'),
    # Архивировать ТС
    path('<int:pk>/archive/', views.VehicleArchiveView.as_view(), name='vehicle_archive'),
    # Восстановить ТС из архива
    path('<int:pk>/unarchive/', views.VehicleUnarchiveView.as_view(), name='vehicle_unarchive'),
    # Директория сотрудников
    path('employees/', views.UserDirectoryView.as_view(), name='user_directory'),
    # Импорт сотрудников из CSV
    path('employees/import/', views.EmployeeImportView.as_view(), name='employee_import'),
    # Расписание ТО-2
    path('maintenance/', views.MaintenanceScheduleView.as_view(), name='maintenance_schedule'),

    # ===== СИСТЕМА (НОВЫЕ МАРШРУТЫ) =====
    # Настройки приложения
    path('settings/', views.SettingsView.as_view(), name='settings'),
    # Справочная информация
    path('about/', views.AboutView.as_view(), name='about'),
    # Свободные гаражные номера
    path('free-garage-numbers/', views.FreeGarageNumbersView.as_view(), name='free_garage_numbers'),
    # Главная страница техническое обслуживание
    path('maintenance-base/', views.MaintenanceBaseView.as_view(), name='maintenance_base'),
    # Главная страница отчётов
    path('reports/', views.ReportsBaseView.as_view(), name='reports_base'),
]

