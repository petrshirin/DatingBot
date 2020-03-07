from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import *

# Create your views here.


def view_profile(request):
    print(request.user)
    return render(request, 'userprofile/profile.html')


def login_user(request, user_id):
    user_profile = UserProfile.objects.filter(user_id=user_id).first()
    if user_profile:
        user = user_profile.user
        login(request, user)
        return redirect('/profile/my/')
    else:
        return render(request, '404.html')
