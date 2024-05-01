from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import customer
from django.db.models import Q
import re



# Create your views here.
# Définir les fonctions a exécuter pour chaque action particuliere
def acceuil(request): 
    context = {}
    if request.user.is_authenticated:
        customer_info = customer.objects.get(username=request.user.username)
        context['customer_info'] = customer_info
    return render(request, 'acceuil.html', context) 


def inscription(request):
    if request.method == "POST":
        # Récupération des données du formulaire
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        birthdate = request.POST.get('birthdate')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        phonenumber = request.POST.get('phonenumber')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        description = request.POST.get('description')
        
        # Validation de l'email
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Veuillez entrer une adresse e-mail valide.')
        
        # Initialisation de la variable pour vérifier toutes les contraintes
        verification_passed = True
        
        # Vérification de correspondance des mots de passe
        if password1 != password2:
            messages.error(request, 'Les deux mots de passe ne correspondent pas.')
            verification_passed = False
        
        # Vérification de la taille du mot de passe
        if len(password1) < 8:
            messages.error(request, 'Le mot de passe doit contenir au moins 8 caractères.')
            verification_passed = False
        
        # Vérification des caractères spéciaux dans le mot de passe
        if not re.search(r'!@#$%^&*(),.?":{}-_|', password1):
            messages.error(request, 'Le mot de passe doit contenir au moins un caractère spécial.')
            verification_passed = False
        
        # Vérification que le mot de passe ne soit pas identique au nom d'utilisateur
        if password1 == username:
            messages.error(request, 'Le mot de passe ne peut pas être identique au nom d\'utilisateur.')
            verification_passed = False
        
        # Vérification de l'existence de l'utilisateur
        if User.objects.filter(Q(email=email) | Q(username=username)).exists():
            messages.error(request, f"Un utilisateur avec l'adresse e-mail {email} ou le nom d'utilisateur {username} existe déjà.")
            verification_passed = False
        
        # Si toutes les vérifications ont été réussies, sauvegarde du client et redirection vers la page de connexion
        if verification_passed:
            # Création de l'utilisateur
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            
            # Création de l'objet customer et sauvegarde des données
            new_customer = customer.objects.create(
                username=username,
                firstname=firstname,
                lastname=lastname,
                birthdate=birthdate,
                gender=gender,
                email=email,
                phonenumber=phonenumber,
                description=description,
            )
            
            # Redirection vers la page de connexion après inscription réussie
            messages.success(request, "Votre compte a été créé avec succès. Vous pouvez maintenant vous connecter.")
            return redirect('connexion')
    
    # Affichage du formulaire d'inscription avec les messages d'erreur si la méthode de requête est POST
    return render(request, 'inscription.html')


def connexion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password) # verifier les infos de user
        if user is not None: # si le user est correctement authentifié il sera connecté
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.') # message d'erreur
    return render(request, 'connexion.html') # sinon renvoi à la page de connexion avec un formulaire vide

def deconnexion(request):
    logout(request)
    return redirect('acceuil')

@login_required
def profile(request):
    context = {}
    if request.user.is_authenticated:
        customer_info = customer.objects.get(username=request.user.username)
        context['customer_info'] = customer_info
    return render(request, 'profile.html', context)