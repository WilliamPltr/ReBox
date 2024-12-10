class SaveLastVisitedURLMiddleware:
    """
    Middleware qui enregistre la dernière URL visitée par l'utilisateur
    dans la session, sauf si elle correspond à certaines URL spécifiques
    comme celles de déconnexion ou d'administration.
    """

    def __init__(self, get_response):
        """
        Initialise le middleware avec la méthode `get_response`.
        Cette méthode est appelée pour traiter chaque requête.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Méthode principale qui gère chaque requête. Enregistre l'URL
        visitée sauf si elle est exclue.
        """
        # Exclure les URLs de déconnexion et celles du panneau admin
        if request.path not in ['/logout/'] and not request.path.startswith('/admin/'):
            request.session['last_visited_url'] = request.path

        # Passer la requête au reste des middlewares et à la vue
        response = self.get_response(request)
        return response
