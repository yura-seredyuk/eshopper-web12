from django.shortcuts import render
from django.contrib.auth.models import User, Group


def profile(request):
   
    return render(request, 'user_profile/profile.html')

