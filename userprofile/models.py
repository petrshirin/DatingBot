from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserRestaurant(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)


class Chat(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=255)
    step = models.IntegerField()


class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    first_name = models.CharField(max_length=255, default=None, blank=True, null=True)
    second_name = models.CharField(max_length=255, default=None, blank=True, null=True)
    photo = models.FileField(default=None, null=True, blank=True, upload_to='image/profile/')
    sex = models.CharField(max_length=20, default=None, null=True, blank=True,)
    age = models.IntegerField(default=None, null=True, blank=True)
    something_about_you = models.TextField(default=None, null=True, blank=True)
    restaurant = models.ForeignKey(UserRestaurant, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.first_name} {self.second_name}'


class UserView(models.Model):
    id = models.AutoField(primary_key=True)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, related_name='+', null=True, blank=True)
    view_user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, related_name='+', null=True, blank=True)
    result = models.BooleanField(default=True)




