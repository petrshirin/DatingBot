from django.shortcuts import render, redirect, HttpResponse
from django.template.response import TemplateResponse
from django.contrib.auth import authenticate, login
from .models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from rest_framework.authtoken.models import Token
from datetime import datetime, timedelta, time
import logging
from base64 import b64decode
from django.core.files.base import ContentFile
# Create your views here.
LOG = logging.getLogger(__name__)


def view_profile(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            user_profile = UserProfile.objects.filter(user=request.user).first()
            return TemplateResponse(request, "userprofile2/edit.html", {'userprofile': user_profile})
        elif request.method == 'POST':
            form = UserProfileForm(request.POST, request.FILES)
            user_profile = UserProfile.objects.filter(user=request.user).first()
            if form.is_valid():
                print(form.data['status'])
                data = form.data
                LOG.debug(data)
                if data['age']:
                    try:
                        user_profile.age = int(data['age'])
                    except ValueError:
                        user_profile.age = None
                user_profile.first_name = data['first_name']
                user_profile.sex = data['sex']
                if data['status']:
                    user_profile.status = data['status']
                else:
                    user_profile.status = ""
                if data['sex'] == 'Мужчина':
                    user_profile.search_for = 'Женщина'
                else:
                    user_profile.search_for = 'Мужчина'

                if request.POST.get('inpFile'):
                    file = b64decode(request.POST['inpFile'])
                    user_profile.photo = ContentFile(file, f'avatar_{user_profile.pk}.png')
                user_profile.save()
                count_new_coincidence = UserCoincidence.objects.filter((Q(user_1=user_profile, is_view_1=False) | Q(user_2=user_profile, is_view_2=False))).count()
                return redirect('/profile/search/', {'userprofile': user_profile, 'countnewcoincidence': count_new_coincidence})
            else:
                return TemplateResponse(request, "userprofile2/edit.html", {'userprofile': user_profile, 'errors': form.errors})
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
            return TemplateResponse(request, "userprofile2/meet.html", {'userprofile': user, 'otheruserprofile': other})
        else:
            coincidences = UserCoincidence.objects.filter((Q(user_1=user_profile) | Q(user_2=user_profile))).all()
            i = 0

            return TemplateResponse(request, "userprofile2/matchList.html", {'userprofile': user_profile, 'userviews': coincidences})
    else:
        return bad_request(request)


@login_required
def view_menu(request):
    user_profile = UserProfile.objects.get(user=request.user)
    count_new_coincidence = UserCoincidence.objects.filter((Q(user_1=user_profile, is_view_1=False) | Q(user_2=user_profile, is_view_2=False))).count()
    return TemplateResponse(request, "userprofile2/menu.html", {'userprofile': user_profile, 'countnewcoincidence': count_new_coincidence})


@login_required
def view_search(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        count_new_coincidence = UserCoincidence.objects.filter((Q(user_1=user_profile, is_view_1=False) | Q(user_2=user_profile, is_view_2=False))).count()
        return TemplateResponse(request, 'userprofile2/search.html', {'userprofile': user_profile, 'countnewcoincidence': count_new_coincidence})
    else:
        return bad_request(request)


def bad_request(request):
    return render(request, 'userprofile/404.html', status=404)


def geo_page_view(request, restaurant_id):
    user_profile = UserProfile(restaurant_id=restaurant_id)
    return render(request, 'userprofile2/geo.html', {'userprofile': user_profile})


def register_user(request, restaurant_id):
    rest = UserRestaurant.objects.filter(pk=restaurant_id).first()
    if not rest:
        return bad_request(request)
    if request.method == 'POST':

        phone = request.POST['tel']
        if not phone:
            return TemplateResponse(request, 'userprofile2/RegTel.html', {"error": "Неверный номер телефона, введите заного"})
        phone = phone.strip()
        user_profile = UserProfile.objects.filter(phone=phone).first()
        LOG.debug(user_profile)
        if user_profile:
            login(request, user_profile.user)
            user_profile.restaurant = rest
            user_profile.save()

            if not user_profile.first_name:
                return redirect('/profile/addname/', {'userprofile': user_profile})

            if not user_profile.photo:
                return redirect('/profile/addphoto/', {'userprofile': user_profile})
            return redirect('/profile/my/', {'userprofile': user_profile})
        else:
            user = User.objects.create_user(phone, password=phone + 'user=' + phone)
            user_profile = UserProfile(user=user, restaurant=rest, phone=phone)
            token = Token(user=user)
            token.save()
            user_profile.save()
            login(request, user)
            return redirect('/profile/addname/', {'userprofile': user_profile})

    elif request.method == 'GET':
        user_profile = UserProfile(restaurant_id=restaurant_id)
        return TemplateResponse(request, 'userprofile2/RegTel.html', {"error": "",
                                                                      "userprofile": user_profile})

    else:
        return bad_request(request)


@login_required
def add_name_sex(request):
    if request.method == 'POST':
        sex = request.POST['sex']
        first_name = request.POST['name']
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.first_name = first_name
        if sex == 'male':
            user_profile.sex = 'Мужчина'
            user_profile.search_for = 'Женщина'
        else:
            user_profile.sex = 'Женщина'
            user_profile.search_for = 'Мужчина'
        user_profile.save()
        return redirect('/profile/addage/', {'userprofile': user_profile})

    elif request.method == 'GET':
        user_profile = UserProfile.objects.get(user=request.user)
        return TemplateResponse(request, 'userprofile2/RegName.html', {"error": "", 'userprofile': user_profile})

    else:
        return bad_request(request)


@login_required
def add_age(request):
    if request.method == 'POST':
        age = request.POST['age']
        user_profile = UserProfile.objects.get(user=request.user)
        if age:
            try:
                user_profile.age = int(age)
            except ValueError:
                user_profile.age = None
            user_profile.save()

        return redirect('/profile/addstatus/', {'userprofile': user_profile})

    elif request.method == 'GET':
        user_profile = UserProfile.objects.get(user=request.user)
        return TemplateResponse(request, 'userprofile2/RegAge.html', {"error": "", 'userprofile': user_profile})

    else:
        return bad_request(request)


@login_required
def add_status(request):
    if request.method == 'POST':
        status = request.POST['me']
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.status = status
        user_profile.save()
        return redirect('/profile/addphoto/', {'userprofile': user_profile})

    elif request.method == 'GET':
        user_profile = UserProfile.objects.get(user=request.user)
        return TemplateResponse(request, 'userprofile2/RegWords.html', {"error": "", 'userprofile': user_profile})

    else:
        return bad_request(request)


@login_required
def add_photo(request):
    if request.method == 'POST':
        file = b64decode(request.POST['inpFile'])
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.photo = ContentFile(file, f'avatar_{user_profile.pk}.png')

        user_profile.save()
        return redirect('/profile/go/', {'userprofile': user_profile})

    elif request.method == 'GET':
        user_profile = UserProfile.objects.get(user=request.user)
        return TemplateResponse(request, 'userprofile2/RegPhoto.html', {"error": "", 'userprofile': user_profile})

    else:
        return bad_request(request)


@login_required
def all_done(request):
    if request.method == 'GET':
        user_profile: UserProfile = UserProfile.objects.get(user=request.user)
        user_profile.is_active = True
        user_profile.save()
        return TemplateResponse(request, 'userprofile2/Go.html', {"userprofile": user_profile})
    else:
        return bad_request(request)


@login_required
def not_users(request):
    if request.method == 'GET':
        user_profile = UserProfile.objects.get(user=request.user)
        profiles = UserProfile.objects.filter(restaurant=user_profile.restaurant,
                                              search_for=user_profile.sex,
                                              sex=user_profile.search_for).all()
        user_views = UserView.objects.filter(user_profile=user_profile).all()
        user_views_list = []
        for user_view in user_views:
            user_views_list.append(user_view.view_user)
        profile = None
        for profile in profiles:
            if profile == user_profile:
                profile = None
                continue
            if profile not in user_views_list:
                if now() - profile.last_active >= timedelta(hours=1):
                    profile.is_active = False
                    profile.save()
                if profile.is_active:
                    break
                else:
                    profile = None
            else:
                profile = None
        count_new_coincidence = UserCoincidence.objects.filter((Q(user_1=user_profile, is_view_1=False) | Q(user_2=user_profile, is_view_2=False))).count()
        if profile:
            return redirect('/profile/search/', {'userprofile': user_profile, 'countnewcoincidence': count_new_coincidence})

        return TemplateResponse(request, 'userprofile2/endOfSearch.html', {"userprofile": user_profile, 'countnewcoincidence': count_new_coincidence})
    else:
        return bad_request(request)


@login_required
def view_restaurants(request):
    if request.method == 'GET':
        user_profile = UserProfile.objects.get(user=request.user)
        return TemplateResponse(request, 'userprofile2/restaurants.html', {"userprofile": user_profile})
    else:
        return bad_request(request)


@login_required
def view_chat(request, chat_id):
    if request.method == 'GET':
        user_profile = UserProfile.objects.get(user=request.user)
        other_user_profile = UserProfile.objects.get(pk=chat_id)
        messages = Message.objects.filter(Q(sender=user_profile, recipient=other_user_profile) | Q(sender=other_user_profile, recipient=user_profile)).order_by('time')
        if len(messages) == 0:

            return TemplateResponse(request, 'userprofile2/emptyChat.html', {"userprofile": user_profile, 'other_userprofile': other_user_profile})
        else:

            for message in messages:
                message.time = (message.time + timedelta(hours=3)).time().strftime('%H:%M')

            return TemplateResponse(request, 'userprofile2/chat.html', {"userprofile": user_profile, 'other_userprofile': other_user_profile, 'messages': messages})

    elif request.method == 'POST':
        text = request.POST['message']
        user_profile = UserProfile.objects.get(user=request.user)
        other_user_profile = UserProfile.objects.get(pk=chat_id)
        messages = Message.objects.filter(Q(sender=user_profile, recipient=other_user_profile) | Q(sender=other_user_profile, recipient=user_profile)).order_by('time')
        messages = list(messages)
        if not messages:
            message = Message(sender=user_profile, recipient=other_user_profile, text=text)
            message.save()
            messages.append(message)

        if len(messages) == 0:

            return TemplateResponse(request, 'userprofile2/emptyChat.html', {"userprofile": user_profile, 'other_userprofile': other_user_profile})
        else:

            for message in messages:
                message.time = message.time.time().strftime('%H:%M')

            return TemplateResponse(request, 'userprofile2/chat.html', {"userprofile": user_profile, 'other_userprofile': other_user_profile, 'messages': messages})

    else:
        return bad_request(request)
