from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.utils import timezone

from titles.models import Genre, Title

from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Модель пользователя
    """
    username = models.CharField(
        unique=True,
        max_length=64,
    )

    email = models.EmailField(
        unique=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=True,
    )

    date_joined = models.DateTimeField(
        default=timezone.now,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)
    PASSWORD_FIELD = 'password'

    objects = UserManager()

    def __str__(self):
        return self.username

    @property
    def is_authenticated(self):
        return True


class History(models.Model):
    """
    Модель истории опроса
    """
    date = models.DateTimeField()

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    title = models.ManyToManyField(
        Title,
        related_name='history_title',
    )

    # class Meta:
    #     constraints = (
    #         UniqueConstraint(
    #             fields=('date', 'user', 'title'),
    #             name='History record must be unique',
    #         ),
    #     )

    def __str__(self):
        return f'{self.user}: ({self.date})'


class LikedTitle(models.Model):
    """
    Модель понравившегося произведения
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    title = models.ManyToManyField(
        Title,
        related_name='liked_title_title',
    )

    # class Meta:
    #     constraints = (
    #         UniqueConstraint(
    #             fields=('user', 'title'),
    #             name='Liked title already exists',
    #         ),
    #     )

    def __str__(self):
        return f'{self.user}: {self.title}'


class DislikedTitle(models.Model):
    """
    Модель не понравившегося произведения
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    title = models.ManyToManyField(
        Title,
        related_name='disliked_title_title',
    )

    # class Meta:
    #     constraints = (
    #         UniqueConstraint(
    #             fields=('user', 'title'),
    #             name='Disliked title already exists',
    #         ),
    #     )

    def __str__(self):
        return f'{self.user}: {self.title}'


class PreferredGenre(models.Model):
    """
    Модель предпочитаемых жанров
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    genre = models.ManyToManyField(
        Genre,
        related_name='preffered_genre_genre',
    )

    # class Meta:
    #     constraints = (
    #         UniqueConstraint(
    #             fields=('user', 'genre'),
    #             name='Preferred genre already exists',
    #         ),
    #     )

    def __str__(self):
        return f'{self.user}: {self.genre}'


class DisfavoredGenre(models.Model):
    """
    Модель не предпочитаемых жанров
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    genre = models.ManyToManyField(
        Genre,
        related_name='disfavored_genre_genre',
    )

    # class Meta:
    #     constraints = (
    #         UniqueConstraint(
    #             fields=('user', 'genre'),
    #             name='Disfavored genre already exists',
    #         ),
    #     )

    def __str__(self):
        return f'{self.user}: {self.genre}'
