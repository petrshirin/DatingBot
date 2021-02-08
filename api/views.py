from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView, Response, Request
from .serializers import *
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from django.core.files.base import File
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from django.apps import apps
from django.utils.timezone import now
from datetime import timedelta
from geopy.distance import geodesic
from userprofile.models import UserRestaurant

# Create your views here.

UserProfile = apps.get_model('userprofile', 'UserProfile')
UserView = apps.get_model('userprofile', 'UserView')
UserCoincidence = apps.get_model('userprofile', 'UserCoincidence')
UserRestaurant = apps.get_model('userprofile', 'UserRestaurant')


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
        for profile in profiles:
            if profile == main_profile:
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


class ChangeRest(APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication, CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, rest_id):
        user_profile = UserProfile.objects.get(user=request.user)
        restaurant = UserRestaurant.objects.filter(pk=rest_id).first()
        user_profile.restaurant = restaurant
        user_profile.save()
        return Response({'status': 'ok'}, status=200)


class ChatInfo(APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication, CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        token = Token.objects.get(user=request.user)
        return Response({'token': token.key, 'user_id': user_profile.pk}, status=200)


@api_view(['POST'])
@permission_classes([AllowAny])
def check_geo_view(request: Request, restaurant_id: int):
    data: dict = request.data
    try:
        restaurant = UserRestaurant.objects.get(pk=restaurant_id)
    except UserRestaurant.DoesNotExist:
        return Response({"error": 'invalid restaurant'}, status=404)
    if data.get('latitude') and data.get('longitude'):
        distance = geodesic((data['latitude'], data['longitude']),
                 (restaurant.latitude, restaurant.longitude)).meters
        print(distance)
        return Response({"distance": distance, "status": distance < 1000}, 200)
