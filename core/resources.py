from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Colis
from django.conf import settings

class ColisResource(resources.ModelResource):
    """
    Classe pour gérer l'import/export des données de Colis avec des champs supplémentaires.
    """
    utilisateur = fields.Field(
        column_name='Utilisateur',
        attribute='utilisateur',
        widget=ForeignKeyWidget(model='auth.User', field='username')
    )
    qr_code_url = fields.Field(
        column_name='Qr code'
    )

    class Meta:
        model = Colis
        skip_unchanged = True  # Ignore les lignes qui n'ont pas changé
        report_skipped = True  # Ajoute les lignes ignorées au rapport
        fields = ('id', 'nombre_utilisations', 'etat', 'status_retour', 'date_derniere_utilisation', 'qr_code_url', 'utilisateur')
        export_order = fields  # Ordre des colonnes à l'export

    def dehydrate_utilisateur(self, obj):
        """
        Retourne le nom d'utilisateur associé au colis ou une chaîne vide si aucun utilisateur.
        """
        return obj.utilisateur.username if obj.utilisateur else ""

    def dehydrate_qr_code_url(self, obj):
        """
        Retourne l'URL complète du QR code, ou une chaîne vide si le QR code n'existe pas.
        """
        if obj.qr_code:
            # Assure que l'URL complète du QR code est retournée
            return f"{settings.SITE_URL}{obj.qr_code.url}"
        return ""
