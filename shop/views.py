from django.shortcuts import render, get_object_or_404
from .models import Product

def homepage(request):
    return render(request, 'pages/index.html')


def shop_page(request):
    products = Product.objects.all()
    return render(request, 'shop/shop.html', {'products':products})


def product_detail_page(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/detail.html', {'product':product})