from django.db import models

# Create your models here.

# The category definition class
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

# The product definition class
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now=True)
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE)

