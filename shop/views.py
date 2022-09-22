from django.shortcuts import render, get_object_or_404
from .models import Product, ProductCategory

def homepage(request):
    return render(request, 'pages/index.html')


def shop_page(request, category_slug=None):
    categories = ProductCategory.objects.all()
    products = Product.objects.all()
    category = None
    
    if category_slug:
        category = ProductCategory.objects.filter(slug=category_slug)[0]
        products = Product.objects.filter(product_category=category).distinct()
    return render(request, 'shop/shop.html', {'products':products,
                                            'categories':categories,
                                            'selected_category': category
                                            })


def product_detail_page(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/detail.html', {'product':product})