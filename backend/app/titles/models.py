from django.db import models
from django.db.models import F, Q
from django.db.models.constraints import CheckConstraint, UniqueConstraint
from django.utils import timezone


class Title(models.Model):
    """
    Модель произведения
    """
    title = models.CharField(
        max_length=255,
    )

    year = models.SmallIntegerField()

    imdb_rating = models.FloatField(
        default=0,
    )

    votes_count = models.IntegerField(
        default=0,
    )

    is_movie = models.BooleanField(
        default=True,
    )

    duration = models.SmallIntegerField(
        blank=True,
        null=True,
    )

    seasons_count = models.SmallIntegerField(
        blank=True,
        null=True,
    )

    class Meta:
        constraints = (
            CheckConstraint(
                check=Q(year__gte=1896) & Q(year__lte=timezone.now().year),
                name=f'Year must be in 1896-{timezone.now().year}',
            ),
            CheckConstraint(
                check=Q(imdb_rating__gte=0) & Q(imdb_rating__lte=10),
                name='Imdb rating must be in 0-10',
            ),
            CheckConstraint(
                check=Q(votes_count__gte=0),
                name='Votes count must be positive',
            ),
            CheckConstraint(
                check=(Q(is_movie=True) & Q(duration__isnull=False) & Q(seasons_count__isnull=True))
                | (Q(is_movie=False) & Q(duration__isnull=True) & Q(seasons_count__isnull=False)),
                name='Duration isn`t correct',
            ),
            CheckConstraint(
                check=Q(duration__gte=0) | Q(seasons_count__gt=0),
                name='Duration or seasons count must be positive',
            ),
        )

    def __str__(self):
        return self.title


class SimilarTitle(models.Model):
    """
    Модель похожих произведений
    """
    title = models.ForeignKey(
        Title,
        related_name='titles',
        on_delete=models.CASCADE,
    )

    similar_title = models.ForeignKey(
        Title,
        related_name='similar_titles',
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=('title', 'similar_title'),
                name='SimilarTitle record already exists',
            ),
            CheckConstraint(
                check=~Q(title=F('similar_title')),
                name='Title and similar_title is the same',
            ),
        )

    def __str__(self):
        return f'{self.title}: {self.similar_title}'


class TitleMixin(models.Model):
    """
    Миксин для классов с отношением к фильму многие-ко-многим
    """
    titles = models.ManyToManyField(Title)

    class Meta:
        abstract = True


class Genre(TitleMixin):
    """
    Модель жанра
    """
    title = models.CharField(
        unique=True,
        max_length=32,
    )

    def __str__(self):
        return self.title


class Director(TitleMixin):
    """
    Модель режиссера
    """
    name = models.CharField(
        max_length=64,
    )

    def __str__(self):
        return self.name


class Country(TitleMixin):
    """
    Модель страны
    """
    title = models.CharField(
        unique=True,
        max_length=64,
    )

    def __str__(self):
        return self.title


class ContentRating(TitleMixin):
    """
    Модель возрастного ограничения
    """
    value = models.SmallIntegerField(
        default=0,
    )

    class Meta:
        constraints = (
            CheckConstraint(
                check=Q(value__gte=0) & Q(value__lte=18),
                name='Content rating value must be in 0-18',
            ),
        )

    def __str__(self):
        return self.value


class Actor(TitleMixin):
    """
    Модель актера
    """
    name = models.CharField(
        max_length=64,
    )

    def __str__(self):
        return self.name


class AdditionalCriteria(TitleMixin):
    """
    Общая модель для всех дополнительных критериев
    """
    title = models.CharField(
        max_length=64,
    )

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class Mood(AdditionalCriteria):
    """
    Модель настроения
    """


class ViewingMethod(AdditionalCriteria):
    """
    Модель способа просмотра
    """


class ViewingTime(AdditionalCriteria):
    """
    Модель времени суток для просмотра
    """


class VisualAtmosphere(AdditionalCriteria):
    """
    Модель визуальной атмосферы
    """


class Audience(AdditionalCriteria):
    """
    Модель аудитории фильма
    """


class Intellectuality(AdditionalCriteria):
    """
    Модель интеллектуальности фильма
    """


class NarrativeMethod(AdditionalCriteria):
    """
    Модель метода повествования
    """


class Acting(AdditionalCriteria):
    """
    Модель игры актеров
    """


class AmountOfDialogue(AdditionalCriteria):
    """
    Модель кол-ва диалогов
    """


class Graphics(AdditionalCriteria):
    """
    Модель графики
    """
