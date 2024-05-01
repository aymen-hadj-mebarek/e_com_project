# pour définir la structur du formulaire
from django import forms
from django.contrib.auth.forms import UserCreationForm
from  .models import *


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password', 
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete' : 'new-password'}),
    )
    password2 = forms.CharField(
        label='Password confirmation', 
        strip=False, 
        widget=forms.PasswordInput(attrs={'autocomplete' : 'new-password'}),
    )

    # personaliser les options du formulaire
    class Meta(UserCreationForm.Meta):
        model = customer
        fields = ['username', 'firstname', 'lastname', 'password', 'birthdate', 'gender', 'email', 'phonenumber', 'picture', 'description', 'balance']