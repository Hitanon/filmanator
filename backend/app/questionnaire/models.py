# import uuid

from config.settings import AUTH_USER_MODEL

from django.db import models
from django.db.models import Q
from django.db.models.constraints import UniqueConstraint

from titles import models as t_models


class Session(models.Model):
    # id = models.UUIDField(
    #     primary_key=True,
    #     default=uuid.uuid4,
    #     auto_created=True,
    #     editable=False,
    # )

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
        return f'{self.id}:{self.user}'


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
    # id = models.UUIDField(
    #     primary_key=True,
    #     default=uuid.uuid4,
    #     auto_created=True,
    #     editable=False,
    # )

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
        default=3,
    )

    answer = models.ManyToManyField(
        Answer,
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


CRITERIONS = {
    'content_rating': t_models.ContentRating,
    'acting': t_models.Acting,
    # 'actor': models.Actor,
    'amount_of_dialogue': t_models.AmountOfDialogue,
    'audience': t_models.Audience,
    'country': t_models.Country,
    # 'director': models.Director,
    'genre': t_models.Genre,
    'graphics': t_models.Graphics,
    'intellectuality': t_models.Intellectuality,
    'mood': t_models.Mood,
    'narrative_method': t_models.NarrativeMethod,
    'viewing_method': t_models.ViewingMethod,
    'viewing_time': t_models.ViewingTime,
    'visual_atmosphere': t_models.VisualAtmosphere,
}


class ResultCriterions:
    def __init__(self):
        self._data = {}

    # Trash property
    @property
    def data(self):
        return self._data

    @data.getter
    def data(self):
        temp = self._data
        keys = [
            'popularity',
            'year',
            'duration',
            'rating',
        ]
        for key in keys:
            if key in temp.keys():
                del temp[key]
        return temp

    def get_limited_criterion(self, criterion):
        return criterion.more, criterion.less

    def get_unlimited_criterion(self, criterion):
        return [CRITERIONS[criterion.title].objects.get(title=criterion.body).id]

    def get_single_criterion(self, criterion):
        if criterion.has_limits:
            return self.get_limited_criterion(criterion)
        return self.get_unlimited_criterion(criterion)

    def add_result(self, result: Result):
        key = result.category.title
        criterions = result.criterion.all()
        if criterions.count() == 1:
            value = self.get_single_criterion(criterions[0])
        else:
            value = [CRITERIONS[criterion.title].objects.get(title=criterion.body).id for criterion in criterions]
        self.data[key] = value


class SkipAnsweredQuestion:
    def __init__(self, session, question, skip_answer):
        self.session = session
        self.question = question
        self.skip_answer = skip_answer
