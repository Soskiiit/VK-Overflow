from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')
    telegram = models.CharField(max_length=64, blank=True, null=True, verbose_name='Telegram')
    github = models.CharField(max_length=64, blank=True, null=True, verbose_name='GitHub')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
