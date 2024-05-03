"""
URL configuration for authentification project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from auth_app import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls), 
    path('', views.acceuil, name= 'acceuil'), #vide pour que cette page soit la page d'accueil du site
    path('inscription/', views.inscription, name= 'inscription'), 
    path('connexion/', views.connexion, name= 'connexion'),
    path('deconnexion/', views.deconnexion, name= 'deconnexion'),
    path('profile/', views.profile, name= 'profile'),
    path('editProfile/', views.editProfile, name= 'editProfile'),
    path('updatePassword/', views.updatePassword, name= 'updatePassword'),
    path('uploadProfilePicture/', views.uploadProfilePicture, name= 'uploadProfilePicture'),
    path('new_product/',views.new_product, name="new_product"),
    path('new_product_image/',views.new_product_image, name="new_product_image"),
    path('product/<int:id>/',views.product, name="About-infos"),
]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)