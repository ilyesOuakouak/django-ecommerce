from unicodedata import name
from django.contrib import admin
from django.urls import path, include
from .views import (
    HomeView,
    ProductDetailView,
    OrderSummaryView,
    add_to_cart,
)


app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name="home_view"),
    path('product/<slug>/', ProductDetailView.as_view(), name="product_detail"),
    path('add-to-cart/<slug>/', add_to_cart, name="add-to-cart"),
    path('order-summary/', OrderSummaryView.as_view(), name="order_summary")

]
