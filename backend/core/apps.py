from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Relating to the entire project."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = 'Основа'
