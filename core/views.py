from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic.edit import FormView
from .models import Colis, Profil
from .forms import LoginForm, CustomUserCreationForm
from .utils import authenticate_by_email


class CustomLoginView(FormView):
    template_name = 'core/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user, backend = authenticate_by_email(email, password)

        if user is not None:
            login(self.request, user, backend=backend)  # Pass the backend explicitly
            next_url = self.request.POST.get('next', '/')
            return redirect(next_url)
        else:
            form.add_error(None, "Les informations saisies ne correspondent à aucun compte. Veuillez réessayer.")
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        next_url = self.request.GET.get('next', '/')

        # Preserve additional logic for Colis URL context
        is_colis_url = next_url.startswith('/colis/')
        next_colis_id = next_url.split('/')[2] if is_colis_url else None

        context['is_colis_url'] = is_colis_url
        context['next_colis_id'] = next_colis_id
        context['next'] = next_url
        return context


def signup(request):
    # Récupérer l'URL "next" depuis la requête GET ou POST
    next_url = request.GET.get('next', request.POST.get('next', '/'))

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Spécifier le backend explicitement
            backend = 'core.utils.EmailBackend'  # Supposons que EmailBackend est utilisé
            login(request, user, backend=backend)  # Connexion avec le backend spécifié
            
            messages.success(request, "Votre compte a été créé avec succès !")
            
            # Redirige vers "next" ou vers "/" par défaut
            return redirect(next_url)
    else:
        form = CustomUserCreationForm()

    return render(request, 'core/signup.html', {
        'form': form,
        'next': next_url,  # Passer "next" à la vue pour le template
    })

@login_required
def account_view(request):
    try:
        profil = Profil.objects.get(utilisateur=request.user)
        
        # Synchroniser le score avec celui de User
        if profil.score != request.user.score:
            profil.score = request.user.score
            profil.save()

        jauge_score = (profil.score / 1000) * 100
        jauge_score = min(jauge_score, 100)
    except Profil.DoesNotExist:
        profil = None
        jauge_score = 0

    return render(request, 'core/account.html', {
        'profil': profil,
        'jauge_score': jauge_score,
    })

def accueil(request):
    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('/')


def scan_colis(request, colis_id):
    colis = get_object_or_404(Colis, id=colis_id)
    message_ecologique = colis.calcul_economie_co2()
    return render(request, 'core/scan_colis.html', {
        'colis': colis,
        'message_ecologique': message_ecologique,
    })


def retour_colis(request, colis_id):
    colis = get_object_or_404(Colis, id=colis_id)

    if request.method == 'POST':
        if request.user.is_authenticated:
            colis.utilisateur = request.user
            colis.status_retour = 'en_attente'
            colis.save()
            messages.success(request, "Colis marqué comme en attente de validation.")
            return redirect('scan_colis', colis_id=colis_id)
        else:
            messages.error(request, "Veuillez créer un compte pour profiter des avantages d'Opack.")
            return redirect('signup', next=f'/colis/{colis_id}/retour/')

    return render(request, 'core/retour_colis.html', {'colis': colis})


def reutiliser_colis(request, colis_id):
    colis = get_object_or_404(Colis, id=colis_id)
    colis.status = 'reutilisé'  # Assuming a 'status' field exists
    colis.save()
    messages.success(request, "Le colis a été marqué comme réutilisé.")
    return redirect('scan_colis', colis_id=colis.id)


def retourner_vendeur(request, colis_id):
    colis = get_object_or_404(Colis, id=colis_id)
    colis.status = 'retourné_vendeur'  # Assuming a 'status' field exists
    colis.save()
    messages.success(request, "Le colis a été marqué comme retourné au vendeur.")
    return redirect('scan_colis', colis_id=colis.id)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', '/')
                return redirect(next_url)
            else:
                form.add_error(None, "Adresse mail ou mot de passe incorrect.")
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})


def test_view(request):
    return render(request, 'core/test.html', {})

from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

from django.utils.http import urlencode

from django.urls import reverse

class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset.html'
    html_email_template_name = 'registration/password_reset_email.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', '/')  # Ajoute le paramètre `next`
        return context

    def form_valid(self, form):
        logger = logging.getLogger(__name__)
        logger.info("form_valid called for password reset.")
        
        # Récupérer le paramètre `next` et le passer au contexte des e-mails
        form.save(
            request=self.request,
            use_https=self.request.is_secure(),
            html_email_template_name=self.html_email_template_name,
            extra_email_context={
                'protocol': 'https' if self.request.is_secure() else 'http',
                'domain': self.request.get_host(),
                'next': self.request.GET.get('next', '/'),
            },
        )
        # Ajout explicite de `next` dans l'URL de redirection
        next_param = self.request.GET.get('next', '/')
        success_url = f"{reverse('password_reset_done')}?next={next_param}"
        return redirect(success_url)

    
    # def form_valid(self, form):
    #     form.save(
    #         request=self.request,
    #         use_https=self.request.is_secure(),
    #         html_email_template_name=self.html_email_template_name,  # Supprimez email_template_name
    #         extra_email_context={
    #             'protocol': 'https' if self.request.is_secure() else 'http',
    #             'domain': self.request.get_host(),
    #             'next': self.request.GET.get('next', '/'),
    #         },
    #     )
    #     return super().form_valid(form)

from django.shortcuts import render
from django.contrib.auth.views import PasswordResetDoneView
import logging

from django.contrib.auth.views import PasswordResetDoneView

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', '/')  # Passe `next` au contexte
        return context


from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse
from django.shortcuts import redirect
import logging

logger = logging.getLogger(__name__)

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hide_header'] = True  # Ajouter la variable pour cacher le header
        return context

    def form_valid(self, form):
        messages.success(self.request, "Votre mot de passe a été réinitialisé avec succès.")
        logger.info("Password reset form invalid. Errors: %s", form.errors)
        return super().form_valid(form)
    
    def get_success_url(self):
        next_param = self.request.GET.get('next', '/')  # Récupérer `next` depuis l'URL
        logger.info("Redirecting to success URL with next: %s", next_param)
        return f"{reverse('password_reset_complete')}?next={next_param}"

from django.contrib.auth.views import PasswordResetCompleteView

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hide_header'] = True  # Ajouter la variable pour cacher le header
        return context

    def post(self, request, *args, **kwargs):
        # Récupérer l'ID du colis soumis
        colis_id = request.POST.get('colis_id', '').strip()

        # Vérifier si le colis existe
        if Colis.objects.filter(id=colis_id).exists():
            # Rediriger vers la page du colis
            return redirect(f'/colis/{colis_id}/')
        else:
            # Réafficher la page avec un message d'erreur
            context = self.get_context_data()
            context['error_message'] = "Veuillez renseigner un ID de colis valide."
            return self.render_to_response(context)
        

def lost_page(request):
    return render(request, 'core/lost.html')

def colis_recherche(request):
    if request.method == 'POST':
        # Récupérer l'ID soumis
        colis_id = request.POST.get('colis_id', '').strip()

        # Vérifier si l'ID existe dans la base de données
        if Colis.objects.filter(id=colis_id).exists():
            # Rediriger vers la page du colis
            return redirect(f'/colis/{colis_id}/')
        else:
            # Revenir à la page avec un message d'erreur
            error_message = "Veuillez renseigner un ID de colis valide."
            return render(request, 'core/lost.html', {'error_message': error_message})
    else:
        # Si la méthode n'est pas POST, retourner la page par défaut
        return redirect('lost')

from django.shortcuts import render

def test_tailwind(request):
    return render(request, 'core/test_tailwind.html')

from django.shortcuts import redirect

def custom_404_view(request, exception):
    """
    Redirige toutes les erreurs 404 vers la page root (/).
    """
    return redirect('/')