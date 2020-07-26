from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.


class UserRestaurant(models.Model):
    name = models.CharField(max_length=255)


class Chat(models.Model):
    user_id = models.CharField(max_length=255)
    username = models.CharField(max_length=255, null=True, default=True)
    step = models.IntegerField()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None, null=True, blank=True)
    first_name = models.CharField(max_length=255, default=None, blank=True, null=True)
    photo = models.FileField(default=None, null=True, blank=True, upload_to='image/profile/')
    sex = models.CharField(max_length=20, default=None, null=True, blank=True)
    age = models.IntegerField(default=None, null=True, blank=True)
    status = models.TextField(default="", null=True, blank=True)
    phone = models.CharField(max_length=20, default=None, null=True, blank=True)
    restaurant = models.ForeignKey(UserRestaurant, on_delete=models.CASCADE, default=None, null=True, blank=True)
    # chat = models.OneToOneField(Chat, on_delete=models.CASCADE, default=None, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    last_active = models.DateTimeField(default=now)
    search_for = models.CharField(max_length=20, default=None, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.phone}'


class UserView(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    view_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    result = models.BooleanField(default=True)
    date = models.DateField(auto_now=True)


class UserCoincidence(models.Model):
    user_1 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    user_2 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    is_view_1 = models.BooleanField(default=False)
    is_view_2 = models.BooleanField(default=False)


class Message(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_sender')
    recipient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_recipient')
    text = models.CharField(max_length=500)
    time = models.DateTimeField(default=now)

