from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse

from product_manager.models import Product, Product_images
from .models import Book
from django.contrib.auth.decorators import login_required


class produit():
    def __init__(self, id, name, price, media):
        self.id = id
        self.name = name
        self.price = price
        self.media = media
        

def index(request): 
    if request.user.is_authenticated:
        print("connected")
        return redirect('/index-connected')
    else:
        print("disconnected")
        prods = []
        for product in Product.objects.all():
            prods.append(produit(product.id, product.name, product.price, Product_images.objects.get(product=product.id).image.url ))
            
        return render(request, "mangalib/index.htm", {'prods' : prods})

@login_required
def index_connected(request): 
    if request.user.is_authenticated :
        print("connected")
    else:
        print("disconnected")
    customer_info = request.session.get('customer_info')
    
    prods = []
    for product in Product.objects.all():
        prods.append(produit(product.id, product.name, product.price, Product_images.objects.get(product=product.id).image.url ))
    return render(request, "mangalib/indexConnected.htm", {'prods' : prods, 'customer_info': customer_info, "id": int(customer_info['id_user']), 'products': Product.objects.all()}, )



def show(request, id_product): 
    return redirect('About-infos', id = id_product)


def add_in_cart(request, id_product): 
    cart = request.session.get('cart', [])
    cart.append(id_product)


    return redirect('mangalib:index')


def panier(request):

   return render(request, "mangalib/panier.htm")


