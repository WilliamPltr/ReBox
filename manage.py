#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """
    Point d'entrée principal pour l'exécution des tâches administratives de Django.
    """
    # Définit le module des paramètres par défaut
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'opack_project.settings')

    try:
        # Importation de la commande pour exécuter les scripts administratifs
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Gestion des erreurs si Django n'est pas correctement installé
        raise ImportError(
            "Impossible d'importer Django. Vérifiez si Django est installé et "
            "disponible dans votre environnement PYTHONPATH. "
            "Avez-vous oublié d'activer un environnement virtuel ?"
        ) from exc

    # Exécute les commandes passées en ligne de commande
    execute_from_command_line(sys.argv)


# Vérifie si le script est exécuté directement
if __name__ == '__main__':
    main()
