from django import forms
from . import models


class RegisterForm(forms.Form):
    username = forms.CharField(required=True, label='Ім`я користувача')
    email = forms.EmailField(required=True, label='Ваш є-мейл')
    password = forms.CharField(required=True, widget=forms.PasswordInput, label='Виберіть пароль')
    password2 = forms.CharField(required=True, widget=forms.PasswordInput, label='Повторіть пароль')

    def clean_password(self):
        if self.data['password'] != self.data['password2']:
            raise forms.ValidationError('Password don\'t match.')
        return self.data['password']

    def clean_username(self):
        if models.User.objects.filter(username__iexact=self.data.get('username').lower()):
            raise forms.ValidationError('Username already taken.')
        return self.data['username']


class LoginForm(forms.Form):
    username = forms.CharField(required=True, label='Введіть ім`я користувача')
    password = forms.CharField(required=True, widget=forms.PasswordInput, label='Введіть пароль')
