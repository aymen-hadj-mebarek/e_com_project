from django.urls import path
from . import views

app_name = "mangalib"
urlpatterns = [
    path('', views.index, name = "index"),
    path('index-connected', views.index_connected, name = "index_connected"),
    path('<int:id_product>', views.show, name = "show"),
    path('add-to-cart/<int:id_product>', views.add_in_cart, name = "add-cart"),
    path('panier/', views.panier, name = "panier"),
   
   
]