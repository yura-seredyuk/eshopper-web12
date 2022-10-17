from django.shortcuts import render
from django.contrib.auth.models import User, Group
from shop.models import Profile, Country


def profile(request):
    user = ''
    profile = ''
    address = ''
    city = ''
    country = ''

    user = request.user
    if user.is_active:
        profile = Profile.objects.filter(user=user).first()
        address = profile.address
        city = address.city
        country = Country.objects.filter(pk=city.country.id).first()

    return render(request, 'user_profile/profile.html', {"user":user,
                                                        "address":address,
                                                        "city":city,
                                                        "profile":profile,
                                                        "country":country})

