from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from sorl.thumbnail import get_thumbnail


class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')
    telegram = models.CharField(max_length=64, default='', verbose_name='Telegram')
    github = models.CharField(max_length=64, default='', verbose_name='GitHub')

    def get_avatar(self):
        if self.avatar:
            return self.avatar.url
        return f'{settings.STATIC_URL}assets/default-avatar.png'

    def get_avatar_thumbnail(self):
        if self.avatar:
            return get_thumbnail(self.avatar, '256x256', crop='center', quality=51)
        return f'{settings.STATIC_URL}assets/default-avatar.png'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
