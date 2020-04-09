import requests
import time
import datetime
import json
import os
import django
from django.db import Error

os.environ["DJANGO_SETTINGS_MODULE"] = 'datingbot.settings'
django.setup()

site_url = 'http://www.tkl.one/'

from userprofile.models import *

TOKEN = ''

ru = {"welcome": '''Привет тут сервисное сообщение приветствия''',
      'name': 'Как вас зовут?',
      'surname': 'Ваша фамилия?',
      'age': 'Сколько вам лет?(можно пропустить, введите 0)',
      'something_about_you': 'Пару слов о себе',
      'is_new': 'Вы уже зарегистрированны?\n1. Да\n2. Нет',
      'not_is_old': 'Такого пользователя нет, Введите свое имя?',
      'is_old': 'Нашел, вот ваша ссылка для входа\n{}',
      'sex': 'Вы мужчина или женщина?\n1. Мужской\n2. Женский',
      'restaurant': 'В каком вы ресторане:\n{}',
      'not_restaurant': 'Такого ресторана нет, выберите еще раз\n{}',
      'complete_registration': 'Данные успешно заполнены, вот ссылка для входа\n\n{}',
      'understand': 'Я вас не понимаю:(',
      }


class TextBack:
    url = 'http://api.textback.io/api'

    def __init__(self, token=TOKEN):
        self.token = token
        self.headers = {"accept": "application/json",
                        'Authorization': f'Bearer {self.token}'}
        self.time_update = (int(datetime.datetime.timestamp(datetime.datetime.now()))) * 1000

    def send_message(self, info):
        res = requests.post(self.url + '/messages', json=info, headers=self.headers)
        print(res.json())

    def get_updates(self, channel_ids, logic):
        try:
            res = requests.get(self.url + f'/chats?from={self.time_update}', headers=self.headers)
            updates = res.json()
        except json.decoder.JSONDecodeError:
            time.sleep(10)
            updates = {'$items': []}
        print(updates)
        for message in updates['$items']:
            if 'w' in message['channel']:
                exit()

            if message['lastMessage']['text'] in ru.values():
                self.time_update = message['lastMessage']['sentTimestamp'] + 1500
                return
            try:
                for channel_id in channel_ids:
                    if message['channelId'] == channel_id:
                        self.logic(message['lastMessage'], logic)
            except Exception as err:
                print(err)

            print(time.ctime(self.time_update // 1000))
            self.time_update = message['lastMessage']['sentTimestamp'] + 1500
            print(time.ctime((message['lastMessage']['sentTimestamp'] + 1000) // 1000))

    @staticmethod
    def generate_message_body(message):
        info = {'channel': message['channel'],
                'chatId': message['chatId'],
                'channelId': message['channelId'],
                'text': '',
                'buttons': [],
                'attachments': [],
                }
        return info

    def logic(self, message, func):
        if func:
            func(self, message)
            time.sleep(1)
        else:
            raise TextBackException()


def whats_app_logic(self, message):
    info = self.generate_message_body(message)
    chat = Chat.objects.filter(user_id=message['chatId']).first()
    if not chat:
        chat = Chat(user_id=message['chatId'], step=0)
        chat.save()
    if message['text'].lower() == 'старт':
        info['text'] = ru.get('welcome')
        self.send_message(info)
        time.sleep(0.5)
        info['text'] = ru.get('is_new')
        self.send_message(info)
        chat.step = 1
        chat.save()

    elif chat.step == 1:
        if message['text'] == '1' or message['text'].lower() == 'да':
            user = UserProfile.objects.filter(user=User.objects.get(username=message['chatId'])).first()
            if user:
                info['text'] = ru.get('is_old').format(f'{site_url}profile/login/{str(chat.user_id)}/')
                self.send_message(info)
                chat.step = 30
                chat.save()
            else:
                user = User.objects.create_user(message['chatId'], password=message['channelId'] + 'user=' + chat.id)

                info['text'] = ru.get('not_is_old')
                self.send_message(info)
                chat.step = 2
                chat.save()

        elif message['text'] == '2' or message['text'].lower() == 'нет':
            try:
                user = User.objects.create_user(message['chatId'], password=str(message['channelId']) + 'user=' + str(chat.id))
            except Error:
                pass
            info['text'] = ru.get('name')
            self.send_message(info)
            chat.step = 2
            chat.save()

    elif chat.step == 2:
        user = User.objects.get_by_natural_key(message['chatId'])
        if user:
            user_profile = UserProfile(user=user, chat=chat, first_name=message['text'])
        else:
            user = User.objects.create_user(message['chatId'], password=message['channelId'] + 'user=' + chat.id)
            user_profile = UserProfile(user=user, chat=chat, first_name=message['text'])
        info['text'] = ru.get('surname')
        self.send_message(info)
        chat.step = 3
        chat.save()
        print(user_profile)
        user_profile.save()

    elif chat.step == 3:
        user_profile = UserProfile.objects.filter(chat__id=chat.id).first()
        print(UserProfile.objects.all())
        user_profile.second_name = message['text']
        info['text'] = ru.get('age')
        self.send_message(info)
        chat.step = 4
        chat.save()
        user_profile.save()

    elif chat.step == 4:
        user_profile = UserProfile.objects.filter(chat=chat).first()
        try:
            age = int(message['text'])
            user_profile.age = message['text']
        except Exception as err:
            print(err)
            user_profile.age = 0
        info['text'] = ru.get('sex')
        self.send_message(info)
        chat.step = 5
        chat.save()
        user_profile.save()

    elif chat.step == 5:
        user_profile = UserProfile.objects.filter(chat=chat).first()
        if message['text'] == '1' or message['text'].lower() == 'мужской':
            user_profile.sex = 'Мужчина'
        elif message['text'] == '2' or message['text'].lower() == 'женский':
            user_profile.sex = 'Женщина'
        else:
            info['text'] = ru.get('understand')
            self.send_message(info)
            return
        info['text'] = ru.get('something_about_you')
        self.send_message(info)
        chat.step = 6
        chat.save()
        user_profile.save()

    elif chat.step == 6:
        user_profile = UserProfile.objects.filter(chat=chat).first()
        user_profile.something_about_you = message['text']
        restaurants = UserRestaurant.objects.all()
        rest_str = ''
        for i in range(len(restaurants)):
            rest_str += f'{i + 1}. {restaurants[i].name}\n'
        info['text'] = ru.get('restaurant').format(rest_str)
        self.send_message(info)
        chat.step = 7
        chat.save()
        user_profile.save()

    elif chat.step == 7:
        user_profile = UserProfile.objects.filter(chat=chat).first()
        restaurants = UserRestaurant.objects.all()
        i = 1
        for restaurant in restaurants:
            if message['text'] == restaurant.name or message['text'] == str(i):
                user_profile.restaurant = restaurant
                break
            i += 1
        if user_profile.restaurant is None:
            rest_str = ''
            for i in range(len(restaurants)):
                rest_str += f'{i + 1}. {restaurants[i].name}\n'
            info['text'] = ru.get('not_restaurant').format(rest_str)
            self.send_message(info)
            return
        info['text'] = ru.get('complete_registration').format(f'{site_url}profile/login/{str(chat.user_id)}/')
        self.send_message(info)
        chat.step = 8
        chat.save()
        user_profile.save()


class TextBackException(Exception):
    pass


if __name__ == '__main__':
    t = TextBack()
    while True:
        try:
            t.get_updates([9989], whats_app_logic)
            time.sleep(0.5)
        except Exception as err:
            print(err)
            continu
