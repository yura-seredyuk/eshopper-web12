from django.shortcuts import render


def homepage(request):
    return render(request, 'pages/index.html')


def shop_page(request):
    return render(request, 'shop/shop.html')