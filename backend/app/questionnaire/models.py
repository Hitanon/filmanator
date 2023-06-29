from config.settings import AUTH_USER_MODEL

from django.db import models
from django.db.models import Q
from django.db.models.constraints import UniqueConstraint

from titles import models as t_models


class Session(models.Model):
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    is_finished = models.BooleanField(
        default=False,
    )

    start_at = models.DateTimeField()

    class Meta:
        constraints = (
            UniqueConstraint(
                condition=Q(user__isnull=False),
                fields=('user', ),
                name='Only one session for auth user',
            ),
        )

    def __str__(self):
        return f'{self.id}:{self.user}'


class ResultTitle(models.Model):
    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
    )

    match_percentage = models.SmallIntegerField(
        default=0,
    )

    title = models.ForeignKey(
        t_models.Title,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.title}:{self.match_percentage}'


class Criterion(models.Model):
    title = models.CharField(
        max_length=64,
    )

    body = models.CharField(
        max_length=64,
    )

    has_limits = models.BooleanField(
        default=False,
    )

    more = models.FloatField(
        blank=True,
        null=True,
    )

    less = models.FloatField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'{self.title}: {self.body}'


class Answer(models.Model):
    body = models.CharField(
        max_length=64,
    )

    is_next = models.BooleanField(
        default=False,
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

    priority = models.SmallIntegerField(
        default=1,
    )

    answer = models.ManyToManyField(
        Answer,
    )

    has_skip_answer = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return f'{self.priority}:{self.body}'


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
        return f'{self.session.id}: {self.question}'


class Result(models.Model):
    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.PROTECT,
    )

    criterion = models.ManyToManyField(
        Criterion,
        blank=True,
    )

    is_skipped = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return f'{self.session.id}:{self.category}'


class SkipAnsweredQuestion:
    def __init__(self, session, question, skip_answer):
        self.session = session
        self.question = question
        self.skip_answer = skip_answer
