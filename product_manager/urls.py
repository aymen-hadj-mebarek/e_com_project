from django.urls import path
from . import views

urlpatterns = [
    # we will specify the home page route, that will be empty adress, and will get  the views.home function, having the name "blog homr"
    path('new_product/',views.new_product, name="Main-Home"),
    path('product/<int:id>/',views.product, name="About-infos")
]