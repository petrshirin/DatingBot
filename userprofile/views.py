from django.shortcuts import render, redirect, HttpResponse
from django.template.response import TemplateResponse
from django.contrib.auth import authenticate, login
from .models import *
from django.db.models import Q

# Create your views here.


def view_profile(request):
    if request.user.is_authenticated:
        print(UserProfile.objects.get(pk=1))
        user_profile = UserProfile.objects.filter(user=request.user).first()
        print(user_profile)
        return TemplateResponse(request, "userprofile/settings.html", {'user': user_profile})
    else:
        return bad_request(request)


def view_message(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        coincidence = UserCoincidence.objects.filter((Q(user_1=user_profile, is_view_1=False) | Q(user_2=user_profile, is_view_2=False))).first()
        if coincidence:
            if coincidence.user_1 == user_profile:
                user = coincidence.user_1
                other = coincidence.user_2
                coincidence.is_view_1 = True
            else:
                user = coincidence.user_2
                other = coincidence.user_1
                coincidence.is_view_2 = True
            coincidence.save()
            return TemplateResponse(request, "userprofile/match.html", {'user': user, 'other': other})
        else:
            return redirect('/profile/search/')
    else:
        return bad_request(request)


def login_user(request, user_id=None):
    if user_id is None:
        return bad_request(request)
    user_profile = UserProfile.objects.filter(chat__user_id=user_id).first()
    if user_profile:
        user = user_profile.user
        login(request, user)
        return redirect('/profile/my/', {'user': user_profile})
    else:
        return bad_request(request)


def view_search(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        return TemplateResponse(request, 'userprofile/browse.html', {'user': user_profile})
    else:
        return bad_request(request)


def view_favourites(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        user_views = UserView.objects.filter(user_profile=user_profile).all()
        return TemplateResponse(request, 'userprofile/favourites.html', {'user': user_profile, 'fav_users': user_views})
    else:
        return bad_request(request)


def bad_request(request):
    return render(request, 'userprofile/404.html', status=404)
