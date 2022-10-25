from tokenize import group
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from shop.models import Profile, Country, Order, Customer, Employee
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
    group = list(user.groups.values_list('name',flat = True))[0]
    if user.is_active:
        profile = Profile.objects.filter(user=user).first()
        address = profile.address
        city = address.city
        country = Country.objects.filter(pk=city.country.id).first()
        date_of_birth = profile.date_of_birth.strftime("%Y-%m-%d")
        if group == "customer":
            customer = Customer.objects.filter(profile=profile).first()
            orders = Order.objects.filter(customer=customer).order_by("-date_of_order").all()
            orders = [item.obj_to_dict() for item in orders]
        elif group == "employee":
            employee = Employee.objects.filter(profile=profile).first()
            employee_orders = Order.objects.filter(employee=employee).order_by("-date_of_order").all()
            opened_orders = Order.objects.filter(status='opened').order_by("-date_of_order").all()
            orders = [item.obj_to_dict() for item in opened_orders] + [item.obj_to_dict() for item in employee_orders]

    else:
        return redirect('myauth:login')
    return render(request, 'user_profile/profile.html', {"user":user,
                                                        "group":group,
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
    print(request.POST["orderid"])
    Order.objects.filter(pk=int(request.POST["orderid"])).first().delete()
    orders = Order.objects.filter(customer=customer).order_by("-date_of_order").all()
    orders = [item.obj_to_dict() for item in orders]
    return HttpResponse(json.dumps(orders), content_type='application/json')


def order_change_button(request):
    print(request.POST)
    order = Order.objects.filter(pk=int(request.POST["orderid"])).first()
    order.quantity = int(request.POST["quantity"])
    order.price = float(request.POST["price"])
    order.save()
    return HttpResponse(json.dumps({"status":"success"}), content_type='application/json')


def edit_profile(request):
    print(request.POST)
    userid = int(request.POST["userid"][0])
    user = User.objects.filter(pk=userid).first()
    if request.POST["firstname"]:
        user.first_name = request.POST["firstname"]
    if request.POST["password"]:
        user.set_password(request.POST["password"])

    profile = Profile.objects.filter(user=user).first()
    
    if request.POST["zip_code"]:
        profile.address.zip_code = request.POST["zip_code"]

    profile.address.save()
    profile.save()
    user.save()
    return HttpResponse(json.dumps({"status":"success"}), content_type='application/json')


def order_status_edit(request):
    print(request.POST)
    order = Order.objects.filter(pk=int(request.POST["orderid"])).first()
    if order.employee is None:
        userid = int(request.POST["userid"][0])
        user = User.objects.filter(pk=userid).first()
        profile = Profile.objects.filter(user=user).first()
        employee = Employee.objects.filter(profile=profile).first()
        order.employee = employee
    order.status = request.POST["status"]
    order.save()
    return HttpResponse(json.dumps({"status":"success"}), content_type='application/json')


def get_customer(request):
    order = Order.objects.filter(pk=int(request.POST["orderid"])).first()
    profile = order.customer.profile
    user = profile.user
    customer_data = {
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        'city_name': profile.address.city.city_name,
        'country': profile.address.city.country.country_name,
        'street': profile.address.street,
        'appartaments': profile.address.appartaments,
        'zip_code': profile.address.zip_code,
        'phone': profile.phone,
    }
    return HttpResponse(json.dumps(customer_data), content_type='application/json')

