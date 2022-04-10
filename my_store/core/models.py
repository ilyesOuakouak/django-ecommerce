from django.conf import settings
from django.db import models
from django.shortcuts import reverse

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

    # add slug field which will be displayed in url
    slug = models.SlugField()

    # A function to get the avsolute url of a product
    def get_absolute_url(self):
        return reverse("core:product_detail", kwargs={"slug": self.slug})
    
    # function to get the add-to-cart url
    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={"slug": self.slug})
    
class OrderProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    # Function to get the total price without any discount
    def get_total_price(self):
        return self.product.price * self.quantity

    # Function to get the total price if there any discount applied
    def get_total_discount_price(self):
        return self.quantity * self.product.discount_price
    
    # Function to get the amount of money saved with discount 
    def get_amount_saved(self):
        return self.get_total_price() - self.get_total_discount_price()
    
    # Function to get the final price 
    def get_final_price(self):
        if self.product.discount_price:
            return self.get_total_discount_price()
        return self.get_total_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderProduct)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    # Funciton to get the total price of the whole order
    def get_total(self):
        total = 0
        for order_product in self.products.all():
            total += order_product.get_final_price()
        
        return total
