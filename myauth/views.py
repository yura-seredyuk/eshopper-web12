from datetime import date, datetime
from django.shortcuts import redirect, render
from myauth.forms import UserLoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from shop.models import Address, Profile, City, Country, Customer



def log_in(request):
    message = ''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('shop:homepage')
        else:
            message = 'Wrong username and/or password!'
    user_login_form = UserLoginForm()
    return render(request, 'myauth/login.html', {'user_login_form':user_login_form,
                                                'message': message})

def log_out(request):
    logout(request)
    return redirect('shop:homepage')

def signin(request):
    if request.method == 'POST':
        print(request.POST)
        user = User.objects.filter(username=request.POST['username'], email=request.POST['email']).first()
        print(user)
        if user is None:
            user_data = {"username": request.POST["username"],
                "password": request.POST["password"],
                "email": request.POST["email"],
                "first_name": request.POST["first_name"],
                "last_name": request.POST["last_name"]}
            user = User.objects.create_user(**user_data)
            city = City.objects.filter(city_name=request.POST["city"]).first()
            country = None
            if city is None:
                country = Country.objects.filter(country_name=request.POST["country"]).first()
                if country is None:
                    country = Country.objects.create(**{'country_name':request.POST["country"]})
                city_data = {'city_name': request.POST["city"],
                            'country': country}
                city = City.objects.create(**city_data)
            address_data = {'street': request.POST["street"],
                            'appartaments': request.POST["appartaments"],
                            'zip_code': request.POST["zipcode"],
                            'city': city}
            address = Address.objects.create(**address_data)
            group = Group.objects.filter(name='customer').first()
            profile_data = {'user': user,
                            'date_of_birth': datetime.strptime(request.POST["date"], '%Y-%m-%d'),
                            'user_group':group,
                            'phone': request.POST["phone"],
                            'address':address}
            profile = Profile.objects.create(**profile_data)
            customer = Customer.objects.create(**{'profile':profile})
            print(user, city, country, address, profile, customer)
            return redirect('myauth:login')
    return render(request, 'myauth/signin.html')
