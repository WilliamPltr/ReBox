import random
import uuid
from django.core.management.base import BaseCommand
from core.models import Colis

class Command(BaseCommand):
    """
    Commande Django pour générer 50 colis avec des valeurs aléatoires.
    Utilisé principalement pour peupler la base de données avec des données fictives
    pendant les tests ou le développement.
    """

    help = "Génère 50 colis avec des valeurs aléatoires"

    def handle(self, *args, **kwargs):
        # Liste des états possibles pour les colis
        etats = ['chez_client', 'en_transit', 'retourne', 'stationnement']
        colis_crees = []

        # Génère 50 colis avec des données aléatoires
        for _ in range(50):
            colis = Colis(
                id=str(uuid.uuid4())[:10],  # ID unique de 10 caractères
                nombre_utilisations=random.randint(0, 100),  # Nombre aléatoire d'utilisations
                etat=random.choice(etats),  # État aléatoire parmi la liste
            )
            colis.generate_qr_code()  # Génère un QR code pour le colis
            colis_crees.append(colis)

        # Sauvegarde en lot pour optimiser les performances
        Colis.objects.bulk_create(colis_crees)

        # Affiche un message de succès dans la console
        self.stdout.write(self.style.SUCCESS("50 colis ont été créés avec succès !"))

