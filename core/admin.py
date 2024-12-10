from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Colis, Transaction, CodePromo, User
from .resources import ColisResource
from django.contrib.auth.admin import UserAdmin

# Administration pour le modèle Colis
@admin.register(Colis)
class ColisAdmin(ImportExportModelAdmin):
    """
    Configuration de l'administration pour le modèle Colis.
    Inclut des actions personnalisées pour marquer les colis comme retournés ou validés.
    """
    resource_class = ColisResource
    list_display = ('id', 'nombre_utilisations', 'etat', 'status_retour', 'date_derniere_utilisation', 'qr_code', 'utilisateur')
    list_filter = ('etat', 'status_retour', 'date_derniere_utilisation')
    search_fields = ('id', 'utilisateur__username')
    readonly_fields = ('qr_code',)
    actions = ['marquer_comme_retourne', 'marquer_comme_valide']

    def marquer_comme_retourne(self, request, queryset):
        """
        Action pour marquer les colis sélectionnés comme "En attente de validation".
        """
        queryset.update(status_retour='en_attente')
        self.message_user(request, "Les colis sélectionnés ont été marqués comme 'En attente de validation'.")

    marquer_comme_retourne.short_description = "Marquer comme 'En attente de validation'"

    def marquer_comme_valide(self, request, queryset):
        """
        Action pour valider les colis sélectionnés via leur méthode dédiée.
        """
        for colis in queryset:
            colis.valider_colis()
        self.message_user(request, "Les colis sélectionnés ont été validés.")

    marquer_comme_valide.short_description = "Valider les colis"

# Administration pour le modèle Transaction
@admin.register(Transaction)
class TransactionAdmin(ImportExportModelAdmin):
    """
    Configuration de l'administration pour le modèle Transaction.
    Permet l'import/export et le filtrage des actions.
    """
    list_display = ('utilisateur', 'colis', 'type_action', 'date_action')
    list_filter = ('type_action', 'date_action')
    search_fields = ('utilisateur__username', 'colis__id')

# Administration pour le modèle CodePromo
@admin.register(CodePromo)
class CodePromoAdmin(ImportExportModelAdmin):
    """
    Administration pour le modèle CodePromo.
    Permet l'import/export et le filtrage des codes.
    """
    list_display = ('code', 'utilisateur', 'date_expiration', 'est_utilise')
    list_filter = ('est_utilise', 'date_expiration')
    search_fields = ('code', 'utilisateur__username')

# Administration personnalisée pour le modèle User
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Administration personnalisée pour le modèle User.
    Exclut les champs inutilisés comme 'date_derniere_connexion' et personnalise l'affichage.
    """
    list_display = ('username', 'email', 'is_staff', 'is_active', 'date_creation', 'score')
    readonly_fields = ('date_creation',)
    list_filter = ('is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login',)}),
    )
