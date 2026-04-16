from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    nickname = forms.CharField(max_length=50, label='Никнейм')

    class Meta:
        model = User
        fields = ['username', 'email', 'nickname', 'password1', 'password2']
        labels = {
            'username': 'Логин',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            user.profile.nickname = self.cleaned_data['nickname']
            user.profile.slug = ''
            user.profile.save()
        return user

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'avatar', 'bio']
        labels = {
            'nickname': 'Никнейм',
            'avatar': 'Аватар',
            'bio': 'Описание',
        }

class BannedAwareAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', strip=False, widget=forms.PasswordInput)

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if hasattr(user, 'profile') and user.profile.is_banned:
            raise forms.ValidationError(
                'Этот аккаунт заблокирован администратором.',
                code='banned',
            )
