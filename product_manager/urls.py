from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # we will specify the home page route, that will be empty adress, and will get  the views.home function, having the name "blog homr"
    path('new_product/',views.new_product, name="new_product"),
    path('new_product_image/',views.new_product_image, name="new_product_image"),
    path('product/<int:id>/',views.product, name="About-infos"),
    path('menu/',views.menu, name="menu")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)