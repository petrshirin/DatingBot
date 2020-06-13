from django import forms


class UserProfileForm(forms.Form):
    first_name = forms.CharField(max_length=255, min_length=1)
    sex = forms.CharField(max_length=10, min_length=7)
    age = forms.IntegerField(required=False)
    status = forms.CharField(max_length=200, required=False)
    photo = forms.ImageField(required=False)




