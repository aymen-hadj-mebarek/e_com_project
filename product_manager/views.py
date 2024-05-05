from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse

from .forms import ProductForm, ProductImageForm
from .models import Product_images, Product
import mangalib

# Create your views here.

# the function below is for the default page that we are going to display, we need to add a parameter "request" so the function will work
def product(request,id):
    request.session["id"] = id
    prod = Product.objects.get(id = id)
    images = Product_images.objects.filter(product = prod)
    
    if prod.seller.id == request.user.id:
        T = 1
    else:
        T = 0    
    return render(request,"product.html", {'product':prod, 'images':images, 'L': len(images), 'T':T})


def new_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        form_image = ProductImageForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()

        request.session["id"] = product.id
        
        return redirect("new_product_image")
    else:
        form = ProductForm()
        return render(request, 'New_product.html', {'form': form})
    
    
def add_image(request, id):    
    request.session["id"] = id
    return redirect("new_product_image")

def del_image(request, id):    
    image = get_object_or_404(Product_images, id=id)
    # Delete the image object
    image.delete()
    return redirect("modif_product", request.session.get("id"))

def delete_product(request, id):    
    product = get_object_or_404(Product, id=id)
    # Delete the product object
    product.delete()
    return redirect("menu")
    
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
    
def modif_product(request, id):
    prod = Product.objects.get(id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=prod)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
                            
        return redirect('About-infos', id)
    else:
        prod = Product.objects.get(id = id)
        form = ProductForm(instance=prod)
        images = Product_images.objects.filter(product = prod)
        return render(request, 'modif_product.html', {'form': form, 'images':images, 'L': len(images), 'product':prod})
    
    
def menu(request):
    posts = Product.objects.all()
    # return render(request, 'menu.html', {'posts' : posts})
    return redirect('/')