from django.urls import path, include
from .views import *

urlpatterns = [
    path('my/', view_profile, name='profile'),
    path('reg/<int:restaurant_id>', register_user, name='register'),
    path('addname/', add_name_sex, name='addname'),
    path('addage/', add_age, name='addage'),
    path('addstatus/', add_status, name='addstatus'),
    path('addphoto/', add_photo, name='addphoto'),
    path('go/', all_done, name='addphoto'),
    path('', view_profile, name='profile'),
    path('search/', view_search, name='search'),
    path('notusers/', not_users, name='addphoto'),
    path('favourites/', view_message, name='favourites'),
    path('menu/', view_menu, name='favourites'),
    path('restaurants/', view_restaurants, name='favourites'),
    path('chat/<int:chat_id>', view_chat, name='chat'),
    path('geo/<int:restaurant_id>', geo_page_view, name='geo')
]
