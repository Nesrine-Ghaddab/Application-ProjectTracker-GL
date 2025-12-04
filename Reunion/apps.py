# Reunion/apps.py
from django.apps import AppConfig

class ReunionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Reunion'

    def ready(self):
        # import signals so they are registered
        import Reunion.signals  # noqa
