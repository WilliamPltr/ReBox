def get_next_url(request):
    """
    Récupère l'URL suivante (next) de la requête.
    
    - Cherche d'abord dans les paramètres GET ou POST.
    - Si aucune URL n'est trouvée, utilise `HTTP_REFERER` comme fallback.
    - Retourne "/" par défaut si aucun fallback n'est disponible.
    """
    next_url = request.GET.get('next') or request.POST.get('next')
    if not next_url:
        next_url = request.META.get('HTTP_REFERER', '/')  # Page précédente ou racine
    return next_url


from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

class EmailBackend(BaseBackend):
    """
    Backend d'authentification personnalisé utilisant l'email et le mot de passe.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authentifie un utilisateur via son email et mot de passe.
        
        - `username` correspond ici à l'email.
        - Retourne l'utilisateur s'il existe et que le mot de passe est correct.
        - Retourne `None` si l'utilisateur n'existe pas ou si l'authentification échoue.
        """
        User = get_user_model()
        try:
            user = User.objects.get(email=username)  # Recherche utilisateur via email
            if user.check_password(password):  # Vérifie le mot de passe
                return user
        except User.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        """
        Récupère un utilisateur via son ID.
        
        - Retourne l'utilisateur s'il existe.
        - Retourne `None` si l'utilisateur n'existe pas.
        """
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


def authenticate_by_email(email, password):
    """
    Fonction utilitaire pour authentifier un utilisateur via l'EmailBackend.
    
    - Retourne une paire `(utilisateur, nom_backend)` si l'authentification réussit.
    - Retourne `(None, None)` si l'authentification échoue.
    """
    backend = EmailBackend()
    user = backend.authenticate(request=None, username=email, password=password)
    return user, 'core.utils.EmailBackend' if user else (None, None)
