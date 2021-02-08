from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *


urlpatterns = [
    path('get_user/', User.as_view(), name='user'),
    path('like_user/<int:pk>/',  LikeUser.as_view(), name='like'),
    path('dislike_user/<int:pk>/',  DislikeUser.as_view(), name='dislike'),
    path('change_rest/<int:rest_id>/',  ChangeRest.as_view(), name='change_rest'),
    path('chat_info/', ChatInfo.as_view(), name='chat_info'),
    path('check_geo/<int:restaurant_id>', check_geo_view, name='geo')
]