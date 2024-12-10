from django.apps import AppConfig

class CoreConfig(AppConfig):
    """
    Configuration de l'application 'core'.
    """
    default_auto_field = 'django.db.models.BigAutoField'  # Utilise ce type d'ID par défaut pour les modèles
    name = 'core'  # Nom de l'application
