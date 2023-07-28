from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    '''Custom user model.'''
    email = models.EmailField(
        _('email address'),
        max_length=254,
        unique=True,
        help_text=_('Required. 254 characters or fewer.')
    )
    first_name = models.CharField(
        _('first name'),
        max_length=150,
        help_text=_('Required. 150 characters or fewer.')
    )
    last_name = models.CharField(
        _('last name'),
        max_length=150,
        help_text=_('Required. 150 characters or fewer.')
    )
    password = models.CharField(
        _('password'),
        max_length=150
    )

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username', 'first_name', 'last_name', 'password'
    ]

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
        ordering = ['id']

    def __str__(self):
        return f'{self.first_name} aka {self.username}'


class Subscribe(models.Model):
    '''Model allows users subscribe to each other.'''
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribed',
        verbose_name=_('Автор')
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name=_('Подписчик')
    )

    class Meta:
        verbose_name = _('Подписка')
        verbose_name_plural = _('Подписки')
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'user'],
                name='unique_subscribtion'
            )
        ]

    def __str__(self):
        return f'Подписка {self.user} на {self.author}'
