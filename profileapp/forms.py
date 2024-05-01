from django import forms 
from .models import * 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm

#class UserRegisterForm(UserCreationForm):
    #email=forms.EmailField()

    #class Meta:
       # model=User
       # feilds =['','' ,'' ,'', '', '', '']

class ProfileChangeForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'gender', 'date_of_birth', 'adresse','description', 'image'] 

