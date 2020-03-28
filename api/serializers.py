from rest_framework.serializers import ModelSerializer
from userprofile.models import *


class UserProfileSerializer(ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('pk', 'first_name', 'age', 'status', 'photo')
