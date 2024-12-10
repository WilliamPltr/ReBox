from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from core import views
from django.contrib.auth.views import LogoutView
from django.conf.urls import handler404
from core.views import (
    CustomLoginView,
    signup,
    account_view,
    accueil,
    scan_colis,
    retour_colis,
    reutiliser_colis,
    retourner_vendeur,
    test_tailwind,
    lost_page,
    colis_recherche,
    custom_404_view,
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,
)


handler404 = custom_404_view

# Définition des URLs principales du projet
urlpatterns = [
    # Page d'accueil par défaut
    path('', lost_page, name='lost'),  # Redirige vers une page d'erreur ou de recherche

    # Formulaire de recherche de colis
    path('colis-recherche/', colis_recherche, name='colis_recherche'),

    # URLs pour l'administration
    path('grappelli/', include('grappelli.urls')),  # Interface Grappelli (si activée)
    path('admin/', admin.site.urls),  # Administration Django

    # Authentification
    path('login/', CustomLoginView.as_view(), name='login'),  # Vue personnalisée pour la connexion
    path('signup/', signup, name='signup'),  # Création de compte
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),  # Déconnexion

    # Gestion des colis
    path('colis/<slug:colis_id>/', scan_colis, name='scan_colis'),  # Vue des détails d'un colis
    path('colis/<slug:colis_id>/retour/', retour_colis, name='retour_colis'),  # Retourner un colis
    path('colis/<slug:colis_id>/reutiliser/', reutiliser_colis, name='reutiliser_colis'),  # Réutiliser un colis
    path('colis/<slug:colis_id>/retour_vendeur/', retourner_vendeur, name='retourner_vendeur'),  # Retour au vendeur

    # Gestion du compte utilisateur
    path('account/', account_view, name='account'),  # Vue du compte utilisateur
    path('accueil/', accueil, name='accueil'),  # Page d'accueil

    # Gestion des mots de passe
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),  # Réinitialisation du mot de passe
    path('password-reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),  # Confirmation de l'envoi
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),  # Confirme la réinitialisation
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),  # Mot de passe réinitialisé

    # Tests et développement
    path('test-tailwind/', test_tailwind, name='test_tailwind'),  # Test de Tailwind CSS
]

# Ajout des fichiers statiques en mode développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf import settings
from django.conf.urls.static import static

