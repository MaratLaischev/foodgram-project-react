from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from foodgram import constants


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    email = models.CharField(
        max_length=constants.MAX_LENGTH_EMAIL, unique=True
    )
    password = models.CharField('Пароль', max_length=constants.MAX_LENGTH_USER)
    first_name = models.CharField(
        'Имя', max_length=constants.MAX_LENGTH_USER, unique=True
    )
    last_name = models.CharField(
        'Фамилия', max_length=constants.MAX_LENGTH_USER, unique=True
    )

    class Meta:
        ordering = ['username']
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username[:constants.RESTRICTION_STRING]

    def clean(self):
        if self.username == 'me':
            raise ValidationError(
                {'username': 'me запрещен в username'})


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followers')

    class Meta:
        ordering = ['user']
        verbose_name = 'подписчик'
        verbose_name_plural = 'Подписчики'
        constraints = [
            models.UniqueConstraint(fields=['user', 'following'],
                                    name='unique_follow')
        ]

    def __str__(self):
        return (
            f'{self.following.username} подписался на {self.user.username}'
        )
