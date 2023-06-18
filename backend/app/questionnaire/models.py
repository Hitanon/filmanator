# import uuid

from config.settings import AUTH_USER_MODEL

from django.db import models
from django.db.models import Q
from django.db.models.constraints import UniqueConstraint


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
        return f'{self.user}: {self.ends_at}'


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
        return self.body


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
        on_delete=models.CASCADE,
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
    )

    def __str__(self):
        return str(self.session)


class ResultCriterions:
    def __init__(self):
        self._data = {}

    # Data property is trash
    @property
    def data(self):
        return self._data

    @data.getter
    def data(self):
        temp = self._data
        keys = ['votes_count']
        for key in keys:
            if key in temp.keys():
                del temp[key]
        return temp

    def get_limited_criterion(self, criterion):
        return criterion.more, criterion.less

    def get_unlimited_criterion(self, criterion):
        return [criterion.id]

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
            value = [criterion.id for criterion in criterions]
        self.data[key] = value
