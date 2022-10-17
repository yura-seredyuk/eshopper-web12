from django.shortcuts import render
from django.contrib.auth.models import User, Group
from shop.models import Profile, Country, Order, Customer
from datetime import datetime


def profile(request):
    user = ''
    profile = ''
    address = ''
    city = ''
    country = ''
    date_of_birth = ''
    orders = []

    user = request.user
    if user.is_active:
        profile = Profile.objects.filter(user=user).first()
        address = profile.address
        city = address.city
        country = Country.objects.filter(pk=city.country.id).first()
        date_of_birth = profile.date_of_birth.strftime("%Y-%m-%d")
        customer = Customer.objects.filter(profile=profile).first()
        orders = Order.objects.filter(customer=customer).all()
    return render(request, 'user_profile/profile.html', {"user":user,
                                                        "address":address,
                                                        "city":city,
                                                        "profile":profile,
                                                        "country":country,
                                                        "date_of_birth":date_of_birth,
                                                        "orders":orders})

