from django.db import models

# Create your models here.

class Author(models.Model): 
    author_name = models.CharField(max_length = 64, unique = True)

class Book(models.Model): 
    book_title = models.CharField(max_length = 32, unique = True)
    book_quantity = models.IntegerField(default = 1)
    book_fk_author = models.ForeignKey(Author, on_delete= models.DO_NOTHING)