from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required
from .models import Order, OrderProduct, Product, Category
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

# Create your views here.

# Here is the home view
class HomeView(ListView):
    model = Product
    template_name = 'home.html'


# Here is the product view
class ProductDetailView(DetailView):
    model = Product
    template_name = 'product.html'


# Here we're adding products into our Cart
@login_required
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    # We create the product if it doesnt exist or get it if it exists
    order_product, created = OrderProduct.objects.get_or_create(product=product, user=request.user, ordered=False)
    order_list = Order.objects.filter(user=request.user, ordered=False)

    if order_list.exists():
        order = order_list[0]
        
        # we need to check if the product is in the order list
        if order.products.filter(product__slug=product.slug).exists():
            order_product.quantity += 1
            order_product.save()
        else:
            order.products.add(order_product)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.products.add(order_product)

    return redirect("core:product_detail", slug=slug)


# Here we display the cart items
class OrderSummaryView(ObjectDoesNotExist, View):
    def get(self, request):
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            
            context = {
                'object': order
            }

            return render(request, 'order_summary.html', context)
        
        except ObjectDoesNotExist:
            return redirect("/")