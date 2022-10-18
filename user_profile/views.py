from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from shop.models import Profile, Country, Order, Customer
from datetime import datetime
from django.http import HttpResponse
import json


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
        orders = Order.objects.filter(customer=customer).order_by("-date_of_order").all()
        orders = [item.obj_to_dict() for item in orders]
    return render(request, 'user_profile/profile.html', {"user":user,
                                                        "address":address,
                                                        "city":city,
                                                        "profile":profile,
                                                        "country":country,
                                                        "date_of_birth":date_of_birth,
                                                        "orders":orders})


def remove_order_button(request):
    print(request.POST)
    userid = int(request.POST["userid"][0])
    user = User.objects.filter(pk=userid).first()
    profile = Profile.objects.filter(user=user).first()
    customer = Customer.objects.filter(profile=profile).first()
    Order.objects.filter(pk=int(request.POST["orderid"][0])).first().delete()
    orders = Order.objects.filter(customer=customer).order_by("-date_of_order").all()
    orders = [item.obj_to_dict() for item in orders]
    return HttpResponse(json.dumps(orders), content_type='application/json')


