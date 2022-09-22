from django.shortcuts import render
from .models import Product

def homepage(request):
    return render(request, 'pages/index.html')


def shop_page(request):
    products = Product.objects.all()
    return render(request, 'shop/shop.html', {'products':products})