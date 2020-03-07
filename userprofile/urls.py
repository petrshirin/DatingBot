from django.urls import path, include
from .views import *

urlpatterns = [
    path('my/', view_profile, name='profile'),
    path('', view_profile, name='profile'),
    path('login/<str: user_id>', login_user, name='login')
]
