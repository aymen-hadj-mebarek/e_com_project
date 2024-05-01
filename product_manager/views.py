from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import ProductForm, ProductImageForm
from .models import Product_images, Product

# Create your views here.

# the function below is for the default page that we are going to display, we need to add a parameter "request" so the function will work
def product(request,id):
    prod = Product.objects.get(id = id)
    images = Product_images.objects.filter(product = prod)
    for i in images:
        print("================================================")
        print(i.image.url)
        print("================================================")
    return render(request,"product.html", {'product':prod, 'images':images})


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
        # return render(request, 'new_image.html', {'form': form_image})
    else:
        form = ProductForm()
        return render(request, 'New_product.html', {'form': form})

def new_product_image(request):
    if request.method == 'POST':
        form = ProductImageForm(request.POST, request.FILES)
        if form.is_valid() :
            image = form.save(commit=False)
            image.product = Product.objects.get(id=request.session.get('id'))
            image.save()
            return render(request, 'product.html')
        else:        
            print("shit")    
            return render(request, 'new_image.html', {'form': form})

    else:
        form = ProductImageForm()
        return render(request, 'new_image.html', {'form': form})
    
def menu(request):
    posts = Product.objects.all()
    for i in posts:
        print(i)
    return render(request, 'menu.html', {'posts' : posts})