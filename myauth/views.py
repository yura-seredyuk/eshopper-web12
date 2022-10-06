from django.shortcuts import render
from myauth.forms import UserLoginForm



def login(request):
    return render(request, 'myauth/login.html')

def logout(request):
    pass

def signin(request):
    return render(request, 'myauth/signin.html')
