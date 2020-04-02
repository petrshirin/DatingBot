from django.shortcuts import render
from rest_framework.views import APIView, Response
from userprofile.models import UserProfile, UserView, UserCoincidence
from .serializers import *
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.


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
        print(profiles)
        print(user_views_list)
        for profile in profiles:
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
