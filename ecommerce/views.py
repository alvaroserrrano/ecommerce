from django.shortcuts import render
from .models import Item
from django.views.generic import ListView, DetailView

def home (request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "ecommerce/home-page.html", context)

def products(request):
    context={
        'items': Item.objects.all()
    }
    return render(request, 'ecommerce/product-page.html', context)

def checkout(request):
    context={
        'items': Item.objects.all()
    }
    return render(request, 'ecommerce/checkout-page.html', context)
