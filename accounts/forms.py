from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm

from .models import Profile


class UserCreateForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields=('email', 'username', 'password1','password2')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].label='Display name'
        self.fields['email'].label='Email address'


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('location', 'profile_img')

class UserForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields=('username',)