from django.contrib import admin
from .models import Product, Product_images
# Register your models here.
admin.site.register(Product_images)
admin.site.register(Product)