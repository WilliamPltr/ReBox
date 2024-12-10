from core.models import Colis

def add_colis_to_context(request):
    """
    Contexte global pour ajouter un colis à partir de l'ID trouvé dans l'URL.
    
    Cette fonction vérifie si l'ID du colis est présent dans les arguments
    de l'URL (`kwargs`). Si c'est le cas, elle tente de récupérer l'objet
    `Colis` correspondant depuis la base de données et le met à disposition
    dans le contexte. Si le colis n'existe pas, elle retourne un contexte vide.

    Args:
        request: L'objet HttpRequest contenant les informations de la requête.

    Returns:
        dict: Un dictionnaire contenant l'objet `Colis` s'il est trouvé, sinon un dictionnaire vide.
    """
    if 'colis_id' in request.resolver_match.kwargs:
        colis_id = request.resolver_match.kwargs.get('colis_id')
        try:
            # Récupérer le colis correspondant à l'ID
            colis = Colis.objects.get(id=colis_id)
            return {'colis': colis}
        except Colis.DoesNotExist:
            # Aucun colis trouvé avec cet ID, ignorer
            pass
    # Retourner un contexte vide si aucun colis n'est trouvé
    return {}
