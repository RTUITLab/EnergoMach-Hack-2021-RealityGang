from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


class User(AbstractUser):
    full_name = models.CharField('Фамилия И.О.', max_length=50)

    # messages = models.ForeignKey('Message', on_delete=models.SET_NULL, verbose_name='Заявки',
    #                              related_name='user', null=True, blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.full_name
