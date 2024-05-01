from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import ProductForm, ProductImageForm

# Create your views here.

# the function below is for the default page that we are going to display, we need to add a parameter "request" so the function will work
def product(request,id):
    return render(request,"product.html")


def new_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        formset = ProductImageForm(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            product = form.save(commit=False)
            product.seller = request.user  # Assign the current user to the seller field
            product.save()
            
            # formset.instance = product
            # formset.save()
            form = ProductForm()
            formset = ProductImageForm()
    else:
        form = ProductForm()
        formset = ProductImageForm()
    return render(request, 'New_product.html', {'form': form, 'formset': formset})


    