from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from ckeditor.fields import RichTextField



class Brand(models.Model):
    Name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.Name


class Product(models.Model):
    title = models.CharField(max_length=100, unique=True)
    price = models.IntegerField(validators=[MinValueValidator(10000)])
    description = RichTextField()
    image = models.ImageField()
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, related_name='sale')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.title
