from django import forms
from django.contrib.auth.forms import UserCreationForm
# from .models import Profile
from django.contrib.auth.models import User



# form to get data for registering new user
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email','password1','password2']


# form to update user data on Profile page
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model =User
        fields =['username','email']  #we can only change username and email

    