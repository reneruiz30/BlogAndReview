from django.apps import AppConfig

#Clase para configurar la aplicación
class BlogappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blogapp'

    def ready(self):
        import blogapp.models  # Importa las señales de models.py
