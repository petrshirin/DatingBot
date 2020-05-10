from django.shortcuts import render
from rest_framework.views import APIView, Response
from userprofile.models import UserProfile, UserView, UserCoincidence
from .serializers import *
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from django.core.files.base import File
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class User(APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        main_profile = UserProfile.objects.filter(user=request.user).first()
        profiles = UserProfile.objects.filter(restaurant=main_profile.restaurant, search_for=main_profile.sex, sex=main_profile.search_for).all()
        user_views = UserView.objects.filter(user_profile=main_profile).all()
        user_views_list = []
        for user_view in user_views:
            user_views_list.append(user_view.view_user)
        profile = None
        print(main_profile.restaurant, main_profile.sex, main_profile.search_for)
        print(user_views_list)
        for profile in profiles:
            if profile == main_profile:
                profile = None
                continue
            if profile not in user_views_list:
                break
            else:
                profile = None
        if profile:
            ser = UserProfileSerializer(profile)
            return Response(ser.data, status=200)
        else:
            return Response({'status': 'fail', 'error': 'Not users'})


class LikeUser(APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        v_userprofile = UserProfile.objects.filter(pk=pk).first()
        if v_userprofile:
            userprofile = UserProfile.objects.filter(user=request.user).first()
            view = UserView(user_profile=userprofile, view_user=v_userprofile, result=True)
            view.save()
            view_other = UserView.objects.filter(user_profile=v_userprofile, view_user=userprofile, result=True).first()
            if view_other:
                conf = UserCoincidence(user_1=v_userprofile, user_2=userprofile)
                conf.save()
            return Response({'status': 'ok'})
        else:
            return Response({'status': 'fail', 'error': 'Not users'})


class DislikeUser(APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        v_userprofile = UserProfile.objects.filter(pk=pk).first()
        if v_userprofile:
            userprofile = UserProfile.objects.filter(user=request.user).first()
            view = UserView(user_profile=userprofile, view_user=v_userprofile, result=False)
            view.save()
            return Response({'status': 'ok'})
        else:
            return Response({'status': 'fail', 'error': 'Not users'})


class Activity(APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.is_active = not user_profile.is_active
        user_profile.save()
        return Response({'status': 'ok'}, status=200)


class ChangeInfo(APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication, CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request):

        restaurant = UserRestaurant.objects.filter(name=request.data['restaurant_name']).first()
        if restaurant:
            request.user.userprofile.restaurant = restaurant
            request.user.userprofile.first_name = request.data['first_name']
            if request.data.get('photo'):
                request.user.userprofile.photo = request.data.get('photo')

            if 'Мужчин' in request.data['search_for']:
                request.user.userprofile.search_for = 'Мужчина'
            if 'Женщин' in request.data['search_for']:
                request.user.userprofile.search_for = 'Женщина'
            request.user.userprofile.save()
            return Response({'status': 'ok'}, status=201)
        else:
            return Response({'status': 'fail'}, status=400)
