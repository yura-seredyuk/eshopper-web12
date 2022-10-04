from itertools import product
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        c_d = form.cleaned_data
        cart.add(product=product,
                quantity=c_d['quantity'],
                update_quantity=c_d['update_quantity'])
    return redirect('cart:shop_cart')

def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect('cart:shop_cart')

def shop_cart(request):
    cart_data = Cart(request)
    return render(request, 'cart/shop-cart.html',
                            {'cart_data':cart_data})