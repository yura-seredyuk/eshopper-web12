from django.shortcuts import redirect, render
from myauth.forms import UserLoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group



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
    return render(request, 'myauth/signin.html')
