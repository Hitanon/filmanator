from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.utils import timezone

from titles.models import Genre, Title

from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
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

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('email',)

    objects = UserManager()

    def __str__(self):
        return self.username

    @property
    def is_authenticated(self):
        return True


class History(models.Model):
    date = models.DateTimeField()

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=('date', 'user', 'title'),
                name='History record must be unique',
            ),
        )

    def __str__(self):
        return f'{self.user}: {self.title} ({self.date})'


class LikedTitle(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=('user', 'title'),
                name='Liked title already exists',
            ),
        )

    def __str__(self):
        return f'{self.user}: {self.title}'


class DislikedTitle(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=('user', 'title'),
                name='Disliked title already exists',
            ),
        )

    def __str__(self):
        return f'{self.user}: {self.title}'


class PreferredGenre(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=('user', 'genre'),
                name='Preferred genre already exists',
            ),
        )

    def __str__(self):
        return f'{self.user}: {self.genre}'


class DisfavoredGenre(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=('user', 'genre'),
                name='Disfavored genre already exists',
            ),
        )

    def __str__(self):
        return f'{self.user}: {self.genre}'
