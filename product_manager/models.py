from django.db import models
from django.contrib.auth.models import User

# Create your models here.
    
class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    description = models.TextField()
    quantity = models.IntegerField()
    price = models.IntegerField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return "Product : " + self.name
    
class   Product_images(models.Model):
    id = models.IntegerField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product_images/")
    