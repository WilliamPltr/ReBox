from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    """
    Backend d'authentification personnalisé permettant de se connecter avec une adresse e-mail
    au lieu d'un nom d'utilisateur.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authentifie un utilisateur à partir de son adresse e-mail et de son mot de passe.

        Args:
            request: L'objet HTTPRequest (peut être `None` pour des appels sans requête).
            username: Adresse e-mail de l'utilisateur (utilisée à la place du nom d'utilisateur).
            password: Mot de passe fourni par l'utilisateur.
            **kwargs: Autres arguments supplémentaires.

        Returns:
            L'objet utilisateur si l'authentification réussit, sinon `None`.
        """
        UserModel = get_user_model()  # Obtient le modèle utilisateur configuré
        try:
            # Recherche un utilisateur avec l'adresse e-mail spécifiée
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            # Retourne `None` si aucun utilisateur avec cet e-mail n'existe
            return None

        # Vérifie si le mot de passe fourni est correct
        if user.check_password(password):
            return user

        # Retourne `None` si le mot de passe est incorrect
        return None
