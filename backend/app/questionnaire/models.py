from config.settings import AUTH_USER_MODEL

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.db.models.constraints import CheckConstraint, UniqueConstraint


class Session(models.Model):
    """
    Модель сессии
    """
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    start_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        constraints = (
            UniqueConstraint(
                condition=Q(user__isnull=False),
                fields=('user', ),
                name='Only one session for auth user',
            ),
        )

    def __str__(self):
        return f'{self.user}: {self.start_at}'


class Category(models.Model):
    """
    Модель категории
    """
    priority = models.SmallIntegerField(
        default=1,
    )

    title = models.CharField(
        unique=True,
        max_length=64,
    )

    class Meta:
        constraints = (
            CheckConstraint(
                check=Q(priority__gte=1) & Q(priority__lte=10),
                name='Priority must be in 1-10',
            ),
        )

    def __str__(self):
        return f'{self.title} (pr={self.priority})'


class Question(models.Model):
    """
    Модель вопроса
    """
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
    )

    body = models.TextField()

    def __str__(self):
        return f'{self.body} Cat: {self.category}'


class Answer(models.Model):
    """
    Модель ответа
    """
    body = models.CharField(
        max_length=64,
    )

    question = models.ManyToManyField(
        Question,
        through='QuestionAnswer',
    )

    is_skip = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return self.body


class Criterion(models.Model):
    """
    Модель критерия
    """
    title = models.CharField(
        max_length=64,
    )

    body = models.CharField(
        max_length=64,
    )

    answer = models.ManyToManyField(
        Answer,
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


class QuestionAnswer(models.Model):
    """
    Промежуточная модель для моделей Question и Answer
    """
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
    )

    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=('question', 'answer'),
                name='answer and question are unique',
            ),
        )

    def clean(self):
        validate_unique_question_answer(self)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Result(models.Model):
    """
    Модель результата
    """
    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
    )

    criterion = models.ForeignKey(
        Criterion,
        on_delete=models.PROTECT,
    )

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=('session', 'category'),
                name='session and category are unique',
            ),
        )

    def __str__(self):
        return f's_id={self.session.pk} : cat={self.category} : crit={self.criterion}'

    def clean(self):
        check_is_criterion_concer_category(self)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


def validate_unique_question_answer(instance):
    """
    Проверка уникальности ответа на вопрос
    """
    if instance.answer.is_skip:
        return
    if QuestionAnswer.objects.filter(
        question=instance.question,
        answer=instance.answer,
    ).exists():
        raise ValidationError('Question and answer are unique when is_skip=False')


def check_is_criterion_concer_category(instance):
    """
    Проверка косвенной принадлежности критерия категории
    """
    answers = instance.criterion.answer.all()
    categories = set([])
    for answer in answers:
        questions = answer.question.all()
        for question in questions:
            categories.add(question.category)
    if instance.category not in categories:
        raise ValidationError('Criterion not in this category')
