from django.db import models
from datetime import date
from django.contrib.auth.models import User
# Création de la table user
class customer(models.Model):
    idcustomer = models.AutoField(primary_key=True) # AutoField est automatiquement unique
    username = models.CharField(max_length=20) # Champ texte pour le nom d'utilisateur de type strin
    firstname = models.CharField(max_length=50, default='')
    lastname = models.CharField(max_length=50, default='')
    password = models.CharField(max_length=128) # Utilisation d'un champ de longueur suffisante pour le mot de passe sécurisé
    birthdate = models.DateField(default=date.today)
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='male') # Champ choix du genre (homme ou femme)
    adress = models.CharField(max_length=128,  default='') # Adresse user 
    email = models.EmailField(default=None) # Champ Email du type EmailField qui vérifie si l'email est valide
    phonenumber = models.CharField(max_length=15, default='', null=True, blank=True) # Champ pour le numéro de téléphone, utilisé CharField pour la flexibilité (certains numéros peuvent contenir des caractères spéciaux)
    picture = models.ImageField( default='user.png',  blank=True) # Image enregistrée dans un champ texte
    description = models.TextField(null=True, blank=True)  # Description libre en cas d'ajout, utilisé TextField pour permettre des descriptions plus longues
    balance = models.IntegerField(default=0)  # Montant de la balance initiale à zéro

    def __str__(self): # Permet d'afficher le nom complet de l'utilisateur dans Django Admin
        return f"{self.firstname} {self.lastname}"
    
    @property
    def imageURL(self):
        try :
            url = self.picture.url
        except:
            url=''
        return url

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    description = models.TextField()
    quantity = models.IntegerField()
    price = models.IntegerField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    # category = models.CharField(max_length=20)    
    def __str__(self):
        return "Product : " + self.name
    
class   Product_images(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/")