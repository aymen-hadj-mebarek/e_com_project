from django import forms
from .models import Product, Product_images

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'quantity', 'price']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),  # Use a textarea widget for the description field
        }

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = Product_images
        fields = ['image']
        labels = {'image': 'Upload Image'}  # Customize the label for the image field

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False  # Allow the image field to be optional
        self.fields['image'].widget.attrs['multiple'] = True  # Allow multiple image uploads

    # Optionally, you can add validation methods here to ensure uploaded images meet certain criteria
