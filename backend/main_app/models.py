from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


class Subsidy(models.Model):
    name = models.CharField('Name', max_length=250, default='none')
    description = models.TextField('Description', max_length=1500, default='none')

    class Meta:
        verbose_name = 'Subsidy'
        verbose_name_plural = 'Subsidies'

    def __str__(self):
        return f'({self.id}) {self.name}'


class User(AbstractUser):
    name = models.CharField('Name', max_length=50, default='none')

    # messages = models.ForeignKey('Message', on_delete=models.SET_NULL, verbose_name='Заявки',
    #                              related_name='user', null=True, blank=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'({self.id}) {self.name}'
