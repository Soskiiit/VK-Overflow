from django.contrib.auth import login, logout
from django.shortcuts import HttpResponse, redirect, render

from .forms import LoginForm, RegistrationForm


def login_view(request):
    message = ''
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                return redirect('homepage')
            message = 'Неверное имя или пароль'
        else:
            message = 'Произошла непредвиденная ошибка'
    return render(request, 'users/login.html', context={'message': message, 'form': form})


def signup_view(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('homepage')
    return render(request, 'users/signup.html', context={'form': form})


def logout_view(request):
    logout(request)
    return redirect('homepage')


def reset_password(request):
    return HttpResponse('<h1>Забыли пароль? Очень-очень жаль!</h1>')
