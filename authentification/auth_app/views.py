from django.contrib import messages
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
        products  =  Product.objects.filter(seller=request.user)
        context={'customer_info': customer_info, 'products': products} 
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
        return redirect('profile')
    
    # Si la méthode de la requête n'est pas POST, affichez le formulaire de modification avec les données du client existant
    return render(request, 'editProfile.html', {'customer_info': customer_instance})


@login_required
def updatePassword(request):
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
            return redirect('profile')

    # Si la méthode n'est pas POST ou si une vérification a échoué, rendre la page updatepassword.html
    return render(request, 'updatePassword.html')


def uploadProfilePicture(request):
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES)
        if form.is_valid():
            customer_instance = get_object_or_404(customer, username=request.user.username)
            customer_instance.picture = form.cleaned_data['picture']
            customer_instance.save()
            return render(request, 'profile.html', {'customer_info': customer_instance})
    else:
        form = ProfilePictureForm()  # Instanciation du formulaire si la méthode n'est pas POST
    return render(request, 'uploadProfilePicture.html', {'form': form})


#Product Views
# the function below is for the default page that we are going to display, we need to add a parameter "request" so the function will work
def product(request,id):
    prod = Product.objects.get(id = id)
    images = Product_images.objects.filter(product = prod)
    return render(request,"product.html", {'product':prod, 'images':images, 'L': len(images)})


def new_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        form_image = ProductImageForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()

        request.session["id"] = Product.objects.count()
        
        return redirect("new_product_image")
    else:
        form = ProductForm()
        return render(request, 'New_product.html', {'form': form})
    
def new_product_image(request):
    if request.method == 'POST':
        form = ProductImageForm(request.POST, request.FILES)
        if form.is_valid():
            for img in request.FILES.getlist('image'):
                image = Product_images(product=Product.objects.get(id=request.session.get('id')), image=img)
                image.save()
                
            return redirect('menu')  # Redirect to product detail page or any other page
        else:
            return render(request, 'new_image.html', {'form': form})
    else:
        form = ProductImageForm()
        return render(request, 'new_image.html', {'form': form})
    
def menu(request):
    posts = Product.objects.all()
    for i in posts:
        print(i)
    return render(request, 'menu.html', {'posts' : posts})