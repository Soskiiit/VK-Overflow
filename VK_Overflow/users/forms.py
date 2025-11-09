from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from users.models import User


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'iconned-input-field', 'placeholder': 'Username/E-mail'}
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'iconned-input-field', 'placeholder': 'Пароль'}
    ))

    def get_user(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        user = authenticate(username=username, password=password)
        return user


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(
            attrs={'class': 'iconned-input-field', 'placeholder': 'Имя пользователя'}
    ))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'iconned-input-field', 'placeholder': 'E-mail'}
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'iconned-input-field', 'placeholder': 'Пароль'}
    ))
    password_repeat = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'iconned-input-field', 'placeholder': 'Повторите пароль'}
    ))

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise ValidationError(
                'Пользователь с таким именем уже существует.',
                code='username_exists'
            )

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                'Пользователь с таким email уже зарегистрирован.',
                code='email_exists'
            )
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 8:
            raise ValidationError(
                'Пароль слишком короткий. Он должен содержать не менее 8 символов.',
                code='password_too_short',
            )

        if password.isdigit():
            raise ValidationError(
                'Пароль не должен состоять только из цифр.',
                code='password_entirely_numeric',
            )

        if password.isalpha():
            raise ValidationError(
                'Пароль не должен состоять только из букв.',
                code='password_entirely_alpha',
            )

        return password

    def clean(self):
        cleaned_data = super().clean()

        if 'password' in cleaned_data and 'password_repeat' in cleaned_data:
            if cleaned_data['password'] != cleaned_data['password_repeat']:
                self.add_error('password_repeat', 'Пароли не совпадают.')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
