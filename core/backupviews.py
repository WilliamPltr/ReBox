from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Colis, Profil
from .forms import LoginForm
from django import forms
from django.views.generic.edit import FormView
from .utils import authenticate_by_email

# Vue personnalisée pour la connexion
class CustomLoginView(FormView):
    template_name = 'core/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        """
        Authentifie l'utilisateur via son email et mot de passe, et redirige vers la page 'next' si disponible.
        """
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate_by_email(email, password)

        if user is not None:
            login(self.request, user)
            next_url = self.request.POST.get('next', '/')
            return redirect(next_url)
        else:
            form.add_error(None, "Les informations saisies ne correspondent à aucun compte. Veuillez réessayer.")
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        """
        Ajoute des données contextuelles spécifiques pour gérer la logique liée à 'next' et 'colis_id'.
        """
        context = super().get_context_data(**kwargs)
        next_url = self.request.GET.get('next', '/')

        is_colis_url = next_url.startswith('/colis/')
        next_colis_id = next_url.split('/')[2] if is_colis_url else None

        context['is_colis_url'] = is_colis_url
        context['next_colis_id'] = next_colis_id
        context['next'] = next_url

        return context

# Vue pour l'inscription d'un nouvel utilisateur
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre compte a été créé avec succès !")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})

# Formulaire de connexion
class LoginForm(forms.Form):
    email = forms.EmailField(label="Adresse mail")
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")

# Vue pour gérer la connexion utilisateur
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

# Vue de test
def test_view(request):
    return render(request, 'core/test.html', {})

# Vue pour afficher les informations du compte utilisateur
@login_required
def account_view(request):
    try:
        profil = Profil.objects.get(utilisateur=request.user)
        jauge_score = (profil.score / 1000) * 100
        jauge_score = min(jauge_score, 100)
    except Profil.DoesNotExist:
        profil = None
        jauge_score = 0

    return render(request, 'core/account.html', {
        'profil': profil,
        'jauge_score': jauge_score,
    })

# Vue pour gérer la redirection vers une URL 'next' ou vers l'accueil
def accueil(request):
    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('/')

# Vue pour afficher les détails d'un colis
def scan_colis(request, colis_id):
    colis = get_object_or_404(Colis, id=colis_id)
    message_ecologique = colis.calcul_economie_co2()
    return render(request, 'core/scan_colis.html', {
        'colis': colis,
        'message_ecologique': message_ecologique,
    })

# Vue pour gérer le retour d'un colis
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

# Vue pour réutiliser un colis
def reutiliser_colis(request, colis_id):
    colis = get_object_or_404(Colis, id=colis_id)
    return render(request, 'core/action_result.html', {'colis': colis, 'message': "Le colis a été marqué comme 'réutilisé'."})

# Vue pour marquer un colis comme retourné au vendeur
def retourner_vendeur(request, colis_id):
    colis = get_object_or_404(Colis, id=colis_id)
    return render(request, 'core/action_result.html', {'colis': colis, 'message': "Le colis a été marqué comme 'retourné au vendeur'."})
