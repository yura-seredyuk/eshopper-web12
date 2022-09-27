from django.shortcuts import render, get_object_or_404
from .models import Product, ProductCategory, Country

def homepage(request):
    categories = ProductCategory.objects.all()
   
    return render(request, 'pages/index.html', {'categories':categories})


def shop_page(request, category_slug=None):
    categories = ProductCategory.objects.all()
    countries = Country.objects.all() 
    products = Product.objects.all()
    selected_category = None

    categories_count = {}
    countries_count = {}
    for country in countries:
        countries_count.update({country.country_name:Product.objects.filter(country=country.id).count()})
    
    selected_categories = []
    if request.method == 'POST':
        print(request.POST.keys())
        for item in request.POST.keys():
            if 'category' in item:
                if item == 'category-all': 
                    category_slug = selected_category = None
                    request.path_info = '/shop/'
                    break
                selected_categories.append(item[9:])

    print(1, selected_categories, category_slug)

    for category in categories:
        categories_count.update({category.category_name:Product.objects.filter(product_category=category.id).count()})

    if len(selected_categories) > 0:
        s_categoryes = ProductCategory.objects.filter(category_name__in=selected_categories)
        products = Product.objects.filter(product_category__in=s_categoryes).distinct()
        category_slug = selected_category = None
        request.path_info = '/shop/'
    elif category_slug:
        selected_category = ProductCategory.objects.filter(slug=category_slug)[0]
        products = Product.objects.filter(product_category=selected_category).distinct()
    print(2, selected_categories, category_slug)
    print(request.path)

    return render(request, 'shop/shop.html', {'products':products,
                                            'categories':categories,
                                            # 'countries':countries,
                                            'selected_category': selected_category,
                                            'countries_count': countries_count,
                                            'categories_count': categories_count
                                            })

def categories_filter(request):
    pass 

def product_detail_page(request, pk):
    categories = ProductCategory.objects.all()

    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/detail.html', {'product':product,
                                            'categories':categories})