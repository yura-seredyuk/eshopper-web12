from django.shortcuts import render


def shop_cart(request):
    return render(request, 'cart/shop-cart.html')