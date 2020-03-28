from django.urls import path, include
from .views import *

urlpatterns = [
    path('my/', view_profile, name='profile'),
    path('', view_profile, name='profile'),
    path(r'login/<str:user_id>/', login_user, name='login'),
    path('search/', view_search, name='search'),
    path('messages/', view_message, name='messages'),
    path('favourites/', view_favourites, name='favourites')
]
