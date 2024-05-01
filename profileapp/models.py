from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    adresse=models.CharField(max_length=50,blank=False, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(default='default.jpg',upload_to='static/images')

    def __str__(self) :
        return f'{self.user.username} profile' 
    
    @property
    def imageURL(self):
        try :
            url = self.image.url
        except:
            url=''
        return url
    
    @property
    def fullName(self):
        return  f'{self.first_name} {self.last_name}'

