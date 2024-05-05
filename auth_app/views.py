from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import customer
from django.db.models import Q
from django.shortcuts import get_object_or_404
import re
from .forms import *
from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import random
from product_manager.models import *

# Create your views here.
# Custumer views 
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
        adress = request.POST.get('adress')
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
                adress=adress,
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
            customer_info = customer.objects.get(username= request.POST['username'])
            request.session['customer_info'] = {
            'id_user': customer_info.idcustomer,
            'firstname': customer_info.firstname,
            'lastname': customer_info.lastname,
            'email': customer_info.email,

            # Ajoutez d'autres données si nécessaire
            }
            login(request, user)
            return redirect('mangalib:index_connected')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect')

    return render(request, 'connexion.html')


@login_required
def deconnexion(request):
    print("deconnexion")
    print(request.user)
    logout(request)
    print(request.user)
    return redirect('mangalib:index')



@login_required
def profile(request, id_user):
    # if request.method == 'POST':
    #     username = request.POST['username']
    #     password = request.POST['password']
    #     user = authenticate(request, username=username, password=password) 
    #     if user is not None: 
    #         print("hey")
    #     else:
    #         return HttpResponse("Hello")
    # else: 

    customer_instance = get_object_or_404(customer, idcustomer = id_user)
    products  = Product.objects.filter(seller=request.user)
    context = {"customer_info": customer_instance,"products": products}
    return render(request, 'profile.html', context)



 


@login_required
def editProfile(request):
    # Récupérez l'objet Customer existant ou renvoyez une erreur 404 si non trouvé
    customer_instance = get_object_or_404(customer, username=request.user.username)
    user = User.objects.get(username=request.user.username)

    if request.method == "POST":
        # Récupérez les données du formulaire depuis la requête POST
        new_username = request.POST.get('username')
        new_firstname = request.POST.get('firstname')
        new_lastname = request.POST.get('lastname')
        new_birthdate = request.POST.get('birthdate')
        #new_gender = request.POST.get('gender')
        new_adress = request.POST.get('adress')
        new_email = request.POST.get('email')
        new_phonenumber = request.POST.get('phonenumber')
        new_description = request.POST.get('description')
        
        # Mettez à jour les champs de l'objet Customer
        customer_instance.username = new_username
        customer_instance.firstname = new_firstname
        customer_instance.lastname = new_lastname
        customer_instance.birthdate = new_birthdate
        #customer_instance.gender = new_gender
        customer_instance.adress = new_adress
        customer_instance.email = new_email
        customer_instance.phonenumber = new_phonenumber
        customer_instance.description = new_description
        
        # Sauvegardez les modifications dans la base de données
        customer_instance.save()
        user.username = new_username
        user.email = new_email
        user.save()
        
        # Redirigez l'utilisateur vers une autre page ou affichez un message de réussite
        return redirect('profile', id_user = customer_instance.idcustomer)
    

    
    print(customer_instance)
    print("Hello world")
    return render(request, 'editProfile.html', {"id":customer_instance.idcustomer, "customer_info": customer_instance })


@login_required
def updatePassword(request):
     
    customer_instance = get_object_or_404(customer, username=request.user.username)
     
    if request.method == "POST":
        password1 = request.POST.get('password1')  # Ancien mot de passe
        password2 = request.POST.get('password2')  # Nouveau mot de passe
        password3 = request.POST.get('password3')  # Confirmation du nouveau mot de passe

        user = request.user  # Récupération de l'utilisateur actuellement connecté

        # Initialisation de la variable pour vérifier toutes les contraintes
        verification_passed = True

        # Vérification que l'ancien mot de passe correspond au mot de passe actuel
        if not user.check_password(password1):
            messages.error(request, 'Veuillez saisir votre ancien mot de passe correctement.')
            verification_passed = False

        # Vérification que les nouveaux mots de passe correspondent
        if password2 != password3:
            messages.error(request, 'Veuillez saisir le même nouveau mot de passe.')
            verification_passed = False

        # Vérification de la taille du nouveau mot de passe
        if len(password2) < 8:
            messages.error(request, 'Le nouveau mot de passe doit contenir au moins 8 caractères.')
            verification_passed = False

        # Vérification des caractères spéciaux dans le nouveau mot de passe
        if not re.search(r'[!@#$%^&*(),.?":{}\-_|]', password2):
            messages.error(request, 'Le nouveau mot de passe doit contenir au moins un caractère spécial.')
            verification_passed = False

        # Vérification que le nouveau mot de passe ne soit pas identique au nom d'utilisateur
        if password2 == user.username:
            messages.error(request, 'Le nouveau mot de passe ne peut pas être identique au nom d\'utilisateur.')
            verification_passed = False

        # Si toutes les vérifications ont réussi, mettre à jour le mot de passe
        if verification_passed:
            user.set_password(password2)
            user.save()
            messages.success(request, 'Votre mot de passe a été mis à jour avec succès.')
            
            return redirect('profile', id_user = customer_instance.idcustomer)

    # Si la méthode n'est pas POST ou si une vérification a échoué, rendre la page updatepassword.html
    return render(request, 'updatePassword.html', {'id': customer_instance.idcustomer})


def uploadProfilePicture(request):
    customer_instance = get_object_or_404(customer, username=request.user.username)
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES)
        if form.is_valid():
            
            customer_instance.picture = form.cleaned_data['picture']
            customer_instance.save()
            return render(request, 'profile.html', {'customer_info': customer_instance})
    else:
        form = ProfilePictureForm()  # Instanciation du formulaire si la méthode n'est pas POST
    return render(request, 'uploadProfilePicture.html', {'id':customer_instance.idcustomer, 'form': form})


def forgetPassword(request):
    if request.method == "POST":

        email = request.POST.get("email")
        user = User.objects.filter(email=email).first()

        if user:
            # print("send email")
            code_confirmation = random.randint(1, 1000)
            contex_email = {'codeEmail':code_confirmation}
            html_text = render_to_string("email.html", contex_email)
            msg = EmailMessage(
                "BoutiqueExpress - Récupération de mot de passe", # l'objet du mail
                html_text,
                "NISCG <yasminearbadji02@gmail.com>", # sender
                [user.email], # receiver
            )
            msg.content_subtype = "html"
            msg.send()
            
            context = {'code':code_confirmation,'email':email}
            print("send email")
            return render(request, "newPassword.html", context)
        else:
            messages.error(request, 'Adresse mail n\'existe pas.') # message d'erreur
            
    return render(request, "forgetPassword.html")


def newPassword(request, code_confirmation, email_confirmation):
    if request.method == "POST": 
        code =  request.POST.get('code') # code de confirmation
        password1 = request.POST.get('password1')  # Nouveau mot de passe
        password2 = request.POST.get('password2')  # Confirmation du nouveau mot de passe

        user = User.objects.filter(email=email_confirmation).first()  # Récupération de l'utilisateur actuellement connecté

        # Initialisation de la variable pour vérifier toutes les contraintes
        verification_passed = True
        
        # verificaztion du code
        if int(code) != int(code_confirmation) :
            messages.error(request, 'Le code ne correspond pas à celui envoyé par e-mail.')
            verification_passed = False


        # Vérification que les nouveaux mots de passe correspondent
        if password1 != password2:
            messages.error(request, 'Veuillez saisir le même nouveau mot de passe.')
            verification_passed = False

        # Vérification de la taille du nouveau mot de passe
        if len(password2) < 8:
            messages.error(request, 'Le nouveau mot de passe doit contenir au moins 8 caractères.')
            verification_passed = False

        # Vérification des caractères spéciaux dans le nouveau mot de passe
        if not re.search(r'[!@#$%^&*(),.?":{}\-_|]', password2):
            messages.error(request, 'Le nouveau mot de passe doit contenir au moins un caractère spécial.')
            verification_passed = False

        # Vérification que le nouveau mot de passe ne soit pas identique au nom d'utilisateur
        if password1 == user.username:
            messages.error(request, 'Le nouveau mot de passe ne peut pas être identique au nom d\'utilisateur.')
            verification_passed = False

        # Si toutes les vérifications ont réussi, mettre à jour le mot de passe
        if verification_passed:
            user.set_password(password1)
            user.save()
            messages.success(request, 'Votre mot de passe a été mis à jour avec succès.')
            return redirect('connexion')

    context = {'code':code_confirmation,'email':email_confirmation}  
    return render(request, "newPassword.html", context)


def updateBalance(request):
     
    customer_instance = get_object_or_404(customer, username=request.user.username)
     
    if request.method == "POST":
        new_balance = request.POST.get('balance')  #  new balance
        password = request.POST.get('password')  # mot de passe
        

        user = request.user  # Récupération de l'utilisateur actuellement connecté

        # Initialisation de la variable pour vérifier toutes les contraintes
        verification_passed = True

        # Vérification que  mot de passe correspond au mot de passe  de user 
        if not user.check_password(password):
            messages.error(request, 'Veuillez saisir votre ancien mot de passe correctement.')
            verification_passed = False

        
        # Si toutes les vérifications ont réussi, mettre à jour  balance 
        if verification_passed:
            customer_instance.balance = new_balance
            customer_instance.save()
            messages.success(request, 'Balance a été mis à jour avec succès.')
            
            return redirect('profile', id_user = customer_instance.idcustomer)

    # Si la méthode n'est pas POST ou si une vérification a échoué, rendre la page updatebalance.html
    return render(request, 'updateBalance.html', {'id': customer_instance.idcustomer})