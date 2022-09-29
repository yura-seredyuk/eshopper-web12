from django.shortcuts import render, get_object_or_404
from .models import Product, ProductCategory, Country
from django.conf import settings


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

    min_price = min(list(map(lambda x: float(x.unit_price), products)))
    max_price = max(list(map(lambda x: float(x.unit_price), products)))
    price_step = (max_price - min_price) / 5
    price_list = [f'${int(min_price + i * price_step)} - ${int(min_price + (i + 1) * price_step - 1)}'  if i != 4 else f'${int(min_price + i * price_step)} - ${int(min_price + (i + 1) * price_step)}' for i in range(5)]
    print(price_list)
    print(Product.objects.filter(unit_price__gte=40, unit_price__lte=50).distinct())
    selected_categories = []
    selected_countries = []

    session = request.session.get(settings.FILTER_SESSION_ID)
    if not session:
        request.session[settings.FILTER_SESSION_ID] = {'selected_categories':[],
                                                        'selected_countries':[],
                                                        'selected_prices': []}
        request.session.modified = True
    session = request.session.get(settings.FILTER_SESSION_ID)

    if request.method == 'POST':
        for item in request.POST.keys():
            if 'category' in item:
                if item == 'category-all': 
                    category_slug = selected_category = None
                    request.path_info = '/shop/'
                selected_categories.append(item[9:])
            if 'country' in item:
                if item == 'country-all': 
                    category_slug = selected_category = None
                    request.path_info = '/shop/'
                selected_countries.append(item[8:])

        if 'all' in selected_categories:
            request.session[settings.FILTER_SESSION_ID]['selected_categories'] = selected_categories = []
            request.session.modified = True
        elif selected_categories != []: 
            request.session[settings.FILTER_SESSION_ID]['selected_categories'] = selected_categories
            request.session.modified = True
        else:
            selected_categories = request.session.get(settings.FILTER_SESSION_ID)['selected_categories']
    
        if 'all' in selected_countries:
            request.session[settings.FILTER_SESSION_ID]['selected_countries'] = selected_countries = []
            request.session.modified = True
        elif selected_countries != []: 
            request.session[settings.FILTER_SESSION_ID]['selected_countries'] = selected_countries
            request.session.modified = True
        else:
            selected_countries = request.session.get(settings.FILTER_SESSION_ID)['selected_countries']
    elif request.method == 'GET':
        del request.session[settings.FILTER_SESSION_ID]



    print(request.session.get(settings.FILTER_SESSION_ID))
    for category in categories:
        categories_count.update({category.category_name:Product.objects.filter(product_category=category.id).count()})

    if len(selected_categories) > 0 and 'all' not in selected_categories:
        s_categoryes = ProductCategory.objects.filter(category_name__in=selected_categories)
        products = Product.objects.filter(product_category__in=s_categoryes).distinct()
        category_slug = selected_category = None
        request.path_info = '/shop/'

    if len(selected_countries) > 0 and 'all' not in selected_countries:
        s_countries = Country.objects.filter(country_name__in=selected_countries)
        products = Product.objects.filter(country__in=s_countries).distinct()
        category_slug = selected_category = None
        request.path_info = '/shop/'

    if category_slug:
        selected_category = ProductCategory.objects.filter(slug=category_slug)[0]
        products = Product.objects.filter(product_category=selected_category).distinct()

    return render(request, 'shop/shop.html', {'products':products,
                                            'categories':categories,
                                            # 'countries':countries,
                                            'selected_category': selected_category,
                                            'countries_count': countries_count,
                                            'categories_count': categories_count,
                                            'selected_categories': selected_categories,
                                            'selected_countries': selected_countries,
                                            'price_list': price_list
                                            })

def categories_filter(request):
    pass 

def product_detail_page(request, pk):
    categories = ProductCategory.objects.all()

    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/detail.html', {'product':product,
                                            'categories':categories})