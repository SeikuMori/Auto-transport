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
]

