from django.apps import AppConfig

class CurralConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'curral'
    def ready(self):
        pass