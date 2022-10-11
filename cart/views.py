from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from django.contrib.auth.models import User
from shop.models import Address, Profile, City, Country, Customer



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
                            {'cart_data':cart_data,
                            'total_price': cart_data.get_total_price(),
                            'cart_quantity':cart_data.__len__()})

def cart_checkout(request):
    cart_data = Cart(request)
    user = request.user
    print(user)
    profile = Profile.objects.filter(user=user).first()
    print(profile)
    customer = Customer.objects.filter(profile=profile).first()
    print(customer)
    address = profile.address
    print(address)
    city = address.city
    print(city)
    country = Country.objects.filter(pk=city.country_id).first() 
    print(country)
    billing_data = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "phone": profile.phone,
        "street": address.street,
        "appartaments": address.appartaments,
        "zip_code": address.zip_code,
        "city": city.city_name,
        "country": country.country_name
    }
    return render(request, 'cart/checkout.html',
                            {'cart_data':cart_data,
                            'total_price': cart_data.get_total_price(),
                            'cart_quantity':cart_data.__len__(),
                            'billing_data': billing_data})