from django.db import models

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    description = models.TextField()
    quantity = models.IntegerField()
    seller = models.ForeignKey(Author, on_delete=models.CASCADE)
    
    def __str__(self):
        return "Product : " + self.name
    
class Product_images(models.Model):
    id = models.IntegerField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products_images/")
    