from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # we will specify the home page route, that will be empty adress, and will get  the views.home function, having the name "blog homr"
    path('new_product/',views.new_product, name="new_product"),
    path('add_image/<int:id>',views.add_image, name="add_image"),
    path('del_image/<int:id>',views.del_image, name="del_image"),
    path('new_product_images/',views.new_product_image, name="new_product_image"),
    path('product/<int:id>/',views.product, name="About-infos"),
    path('modify_product/<int:id>/',views.modif_product, name="modif_product"),
    path('delete_product/<int:id>/',views.delete_product, name="delete_product"),
    path('menu/',views.menu, name="menu")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)