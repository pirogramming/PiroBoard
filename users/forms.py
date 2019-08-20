from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Interest, Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    phone_number = forms.CharField()
    region = forms.CharField()
    nickname = forms.CharField()

    # interests = forms.ModelChoiceField()
    # forms.ModelMultipleChoiceField(queryset=Interest.objects.all(), to_field_name='profile')

    class Meta:
        model = User

        fields = ['username', 'email', 'phone_number', 'region', 'nickname', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(UserRegisterForm, self).__init__(*args, **kwargs)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'group',)
