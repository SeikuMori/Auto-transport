from django.apps import AppConfig


class CardsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cards'

    def ready(self):
        """Регистрируем signals при готовности приложения"""
        import cards.signals  # noqa
