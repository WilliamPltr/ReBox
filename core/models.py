import qrcode
import uuid
from io import BytesIO
from django.db import models
from django.core.files.base import ContentFile
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from django.conf import settings
from django.shortcuts import reverse


# --- Modèle utilisateur personnalisé ---
class User(AbstractUser):
    email = models.EmailField(unique=True)  # Adresse email unique
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    colis_en_attente = models.BooleanField(default=False, verbose_name="Colis en attente de validation")
    score = models.PositiveIntegerField(default=0, verbose_name="Score (sur 1000)")

    def __str__(self):
        return self.email


# --- Signal pour créer un profil lors de la création d'un utilisateur ---
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    from .models import Profil  # Importation locale pour éviter les importations circulaires
    if created:
        Profil.objects.create(utilisateur=instance)
    elif not hasattr(instance, 'profil'):
        Profil.objects.create(utilisateur=instance)


# --- Modèle Profil ---
class Profil(models.Model):
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE)  # Liaison unique avec l'utilisateur
    score = models.IntegerField(default=0, verbose_name="Score utilisateur")  # Score par défaut

    def __str__(self):
        return f"{self.utilisateur.username} - Score: {self.score}"


# --- Générateur d'IDs courts ---
def generate_short_id():
    return str(uuid.uuid4())[:10]


# --- Modèle Colis ---
class Colis(models.Model):
    STATUS_CHOICES = [
        ('en_attente', 'En attente de validation'),
        ('validé', 'Validé'),
        ('aucun', 'Aucun'),
    ]

    utilisateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    nombre_utilisations = models.IntegerField(default=0)
    status_retour = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aucun')
    is_validated = models.BooleanField(default=False, verbose_name="Colis validé")
    id = models.CharField(max_length=100, primary_key=True, default=generate_short_id)  # ID unique généré automatiquement
    etat = models.CharField(max_length=100, default='nouveau')
    date_derniere_utilisation = models.DateTimeField(null=True, blank=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def generate_qr_code(self, request=None):
        """
        Génère un QR code avec l'URL du colis.
        Si `request` n'est pas fourni, une URL de base est utilisée.
        """
        base_url = "http://127.0.0.1:8000/"  # Adresse de votre site en production

        # Construire l'URL selon la disponibilité de `request`
        if request:
            url = request.build_absolute_uri(reverse("scan_colis", kwargs={"colis_id": self.id}))
        else:
            url = f"{base_url}/colis/{self.id}"

        # Générer le QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill="black", back_color="white")

        # Sauvegarder le QR code en tant qu'image
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        self.qr_code.save(f"{self.id}.png", ContentFile(buffer.getvalue()), save=False)
        buffer.close()


    def calcul_economie_co2(self):
        """
        Calcule l'économie de CO2 générée par ce colis.
        """
        economie_co2 = (0.56 * self.nombre_utilisations) - 4.6
        if self.nombre_utilisations >= 9:
            return f"🌱 Well done! Your package has already saved {economie_co2:.2f} kg of CO2 🎉"
        return None

    def valider_colis(self):
        """
        Valide le colis, met à jour l'utilisateur et réinitialise son état.
        """
        if self.utilisateur:
            self.utilisateur.score += 100
            self.utilisateur.save()

        self.nombre_utilisations += 1
        self.utilisateur = None
        self.status_retour = "aucun"
        self.save()

    def __str__(self):
        return f"Colis {self.id} (Statut: {self.status_retour})"


# --- Modèle Transaction ---
class Transaction(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    colis = models.ForeignKey(Colis, on_delete=models.CASCADE)
    type_action = models.CharField(
        max_length=50,
        choices=[
            ('retour', 'Retour'),
            ('reutilisation', 'Réutilisation'),
            ('retour_vendeur', 'Retour au vendeur'),
        ],
    )
    date_action = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        utilisateur_nom = self.utilisateur.username if self.utilisateur else "Utilisateur inconnu"
        return f"{self.type_action} par {utilisateur_nom} le {self.date_action}"


# --- Modèle CodePromo ---
class CodePromo(models.Model):
    code = models.CharField(max_length=20, unique=True)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    date_expiration = models.DateField()
    est_utilise = models.BooleanField(default=False)

    def __str__(self):
        return f"Code {self.code} pour {self.utilisateur.username}"
