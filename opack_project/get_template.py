from django.template.loader import get_template

# Ce script affiche les chemins complets des templates de réinitialisation de mot de passe.

# Chargement et affichage du template de demande de réinitialisation
try:
    template_reset = get_template('registration/password_reset.html')
    print("Template trouvé : registration/password_reset.html")
    print(template_reset)
except Exception as e:
    print("Erreur : Impossible de charger le template 'password_reset.html'")
    print(e)

# Chargement et affichage du template de confirmation d'envoi
try:
    template_reset_done = get_template('registration/password_reset_done.html')
    print("\nTemplate trouvé : registration/password_reset_done.html")
    print(template_reset_done)
except Exception as e:
    print("Erreur : Impossible de charger le template 'password_reset_done.html'")
    print(e)

# Chargement et affichage du template de confirmation de réinitialisation
try:
    template_reset_confirm = get_template('registration/password_reset_confirm.html')
    print("\nTemplate trouvé : registration/password_reset_confirm.html")
    print(template_reset_confirm)
except Exception as e:
    print("Erreur : Impossible de charger le template 'password_reset_confirm.html'")
    print(e)

# Chargement et affichage du template final après réinitialisation
try:
    template_reset_complete = get_template('registration/password_reset_complete.html')
    print("\nTemplate trouvé : registration/password_reset_complete.html")
    print(template_reset_complete)
except Exception as e:
    print("Erreur : Impossible de charger le template 'password_reset_complete.html'")
    print(e)
