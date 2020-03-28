from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('get_user/', User.as_view(), name='user'),
    path('like_user/<int:pk>/',  LikeUser.as_view(), name='like'),
    path('dislike_user/<int:pk>/',  LikeUser.as_view(), name='like'),
    path('change_activity/', Activity.as_view(), name='activity'),
]