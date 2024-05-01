from django.contrib import admin
from django.urls import path 
from . import views
urlpatterns = [
    path('profile/',views.userprofile, name="userprofile"),
    path('editprofile/',views.editprofile, name="editprofile"),
]