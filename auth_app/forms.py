# pour définir la structur du formulaire
from django import forms
from django.contrib.auth.forms import UserCreationForm
from  .models import *

# customer forms 
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
        fields = ['username', 'firstname', 'lastname', 'password', 'birthdate', 'gender', 'adress', 'email', 'phonenumber', 'picture', 'description', 'balance']

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = customer
        fields = ['picture']
        labels = {'image': 'Upload Image'}  # Customize the label for the image field
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['image'].required = False  # Allow the image field to be optional

#product forms 
# class ProductForm(forms.ModelForm):
#     class Meta:
#         fields = ['name', 'description', 'quantity', 'price']
#         widgets = {
#             'description': forms.Textarea(attrs={'rows': 4}),  # Use a textarea widget for the description field
#         }

# class ProductImageForm(forms.ModelForm):
#     class Meta:
#         fields = ['image']
#         labels = {'image': 'Upload Image'}  # Customize the label for the image field

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['image'].required = False  # Allow the image field to be optional
#         self.fields['image'].widget.attrs['multiple'] = True  # Allow multiple image uploads

#     # Optionally, you can add validation methods here to ensure uploaded images meet certain criteria
