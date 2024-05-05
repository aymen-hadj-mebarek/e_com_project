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
    path('profile/<int:id_user>', views.profile, name= 'profile'),
    path('editProfile/', views.editProfile, name= 'editProfile'),
    path('updatePassword/', views.updatePassword, name= 'updatePassword'),
    path('uploadProfilePicture/', views.uploadProfilePicture, name= 'uploadProfilePicture'),
    path('forgetPassword/', views.forgetPassword, name= 'forgetPassword'),
    path('newPassword/<int:code_confirmation>/<str:email_confirmation>', views.newPassword, name= 'newPassword'),
    path('updateBalance/', views.updateBalance, name= 'updateBalance')
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)