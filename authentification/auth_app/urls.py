from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.acceuil, name= 'acceuil'), #vide pour que cette page soit la page d'accueil du site
    path('inscription/', views.inscription, name= 'inscription'), 
    path('connexion/', views.connexion, name= 'connexion'),
    path('deconnexion/', views.deconnexion, name= 'deconnexion'),
    path('profile/', views.profile, name= 'profile'),
    path('new_product/',views.new_product, name="new_product"),
    path('new_product_image/',views.new_product_image, name="new_product_image"),
    path('product/<int:id>/',views.product, name="About-infos"),
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)