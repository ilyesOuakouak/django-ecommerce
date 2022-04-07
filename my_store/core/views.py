from django.shortcuts import render
from django.views.generic import ListView
from .models import Product, Category

# Create your views here.

def home(request):
    context = {
        'name': 'MyStore'
    }

    return render(request, 'home.html', context)


class HomeView(ListView):
    model = Product
    template_name = 'home.html'
