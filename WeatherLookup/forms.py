from django.forms import ModelForm, TextInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import EmailInput
from django import forms
from .models import City


class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {'name': TextInput(attrs={'class': 'input', 'placeholder': 'City name'})}


class CreateUserForm(UserCreationForm):
    def clean_username(self):
        if User.objects.filter(username=self.data['username']).exists():
            self.add_error('username', error='Username already in use')
        return self.data['username']

    def clean(self):
        if self.data['password1'] != self.data['password2']:
            self.add_error(None, error='Passwords should match.')
        return super().clean()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput, label='New Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label="Repeat password")

    def clean(self):
        if self.data['password1'] != self.data['password2']:
            self.add_error(None, error='Passwords need to be identical')
        return super().clean()


class ChangeProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'email': EmailInput(),
        }
        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'Email address',
        }
