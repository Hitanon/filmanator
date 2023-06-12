from config.settings import AUTH_USER_MODEL

from django.db import models
from django.db.models import Q
from django.db.models.constraints import UniqueConstraint


class Session(models.Model):
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    ends_at = models.DateTimeField()

    class Meta:
        constraints = (
            UniqueConstraint(
                condition=Q(user__isnull=False),
                fields=('user', ),
                name='Only one session for auth user',
            ),
        )

    def __str__(self):
        return f'{self.user}: {self.ends_at}'


class Criterion(models.Model):
    title = models.CharField(
        max_length=64,
    )

    body = models.CharField(
        max_length=64,
    )

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=('title', 'body'),
                name='title and body are unique',
            ),
        )

    def __str__(self):
        return f'{self.title}: {self.body}'


class Answer(models.Model):
    body = models.CharField(
        max_length=64,
    )

    is_skip = models.BooleanField(
        default=False,
    )

    criterion = models.ManyToManyField(
        Criterion,
    )

    def __str__(self):
        return self.body


class Question(models.Model):
    body = models.TextField()

    answer = models.ManyToManyField(
        Answer,
    )

    def __str__(self):
        return self.body


class Category(models.Model):
    priority = models.SmallIntegerField(
        default=1,
    )

    title = models.CharField(
        unique=True,
        max_length=64,
    )

    question = models.ManyToManyField(
        Question,
    )

    def __str__(self):
        return f'{self.title} (pr={self.priority})'


class SessionState(models.Model):
    session = models.OneToOneField(
        Session,
        on_delete=models.CASCADE,
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'{self.session}: {self.question}'


class Result(models.Model):
    session = models.ForeignKey(
        Session,
        on_delete=models.PROTECT,
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    criterion = models.ManyToManyField(
        Criterion,
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.session)
