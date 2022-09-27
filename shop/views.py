from django.shortcuts import render, get_object_or_404
from .models import Product, ProductCategory, Country

def homepage(request):
    categories = ProductCategory.objects.all()
   
    return render(request, 'pages/index.html', {'categories':categories})


def shop_page(request, category_slug=None):
    categories = ProductCategory.objects.all()
    countries = Country.objects.all() 
    products = Product.objects.all()
    category = None

    categories_count = {}
    countries_count = {}
    for country in countries:
        countries_count.update({country.country_name:Product.objects.filter(country=country.id).count()})

    for category in categories:
        categories_count.update({category.category_name:Product.objects.filter(product_category=category.id).count()})
    print(categories_count)
    if category_slug:
        category = ProductCategory.objects.filter(slug=category_slug)[0]
        products = Product.objects.filter(product_category=category).distinct()
    return render(request, 'shop/shop.html', {'products':products,
                                            # 'categories':categories,
                                            # 'countries':countries,
                                            'selected_category': category,
                                            'countries_count': countries_count,
                                            'categories_count': categories_count
                                            })


def product_detail_page(request, pk):
    categories = ProductCategory.objects.all()

    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/detail.html', {'product':product,
                                            'categories':categories})