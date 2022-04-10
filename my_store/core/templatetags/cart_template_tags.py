from django import template
from core.models import Order

register = template.Library()

# Function to get the number of items in the cart when the user is authenticated
@register.filter
def number_of_cart_products(user):
    if user.is_authenticated:
        query_set = Order.objects.filter(user=user, ordered=False)
        if query_set.exists():
            return query_set[0].products.count()
    return 0


