from django.db import models
from django.db.models import F, Q
from django.db.models.constraints import CheckConstraint, UniqueConstraint
from django.utils import timezone


class Actor(models.Model):
    """
    Модель актера
    """
    name = models.CharField(
        max_length=64,
    )

    def __str__(self):
        return self.name


class Director(models.Model):
    """
    Модель режиссера
    """
    name = models.CharField(
        max_length=64,
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    """
    Модель жанра
    """
    title = models.CharField(
        unique=True,
        max_length=32,
    )

    def __str__(self):
        return self.title


class Country(models.Model):
    """
    Модель страны
    """
    title = models.CharField(
        unique=True,
        max_length=64,
    )

    def __str__(self):
        return self.title


class ContentRating(models.Model):
    """
    Модель возрастного ограничения
    """
    title = models.CharField(
        unique=True,
        max_length=4,
    )

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
        return self.title


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

    director = models.ManyToManyField(
        Director,
        through='TitleDirector',
        related_name='title_director',
    )

    country = models.ManyToManyField(
        Country,
        through='TitleCountry',
        related_name='title_country',
    )

    actor = models.ManyToManyField(
        Actor,
        through='TitleActor',
        related_name='title_actor',
    )

    genre = models.ManyToManyField(
        Genre,
        through='TitleGenre',
        related_name='title_genre',
    )

    content_rating = models.ForeignKey(
        ContentRating,
        on_delete=models.PROTECT,
        related_name='title_content_rating',
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
                name='Duration isnt correct',
            ),
            CheckConstraint(
                check=Q(duration__gte=0) & Q(seasons_count__gt=0),
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


class TitleModelMixin(models.Model):
    """
    Модель миксин с внешним ключом произведением title
    """
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class TitleDirector(TitleModelMixin):
    """
    Промежуточная модель для моделей Title и Director
    """
    director = models.ForeignKey(
        Director,
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=('title', 'director'),
                name='Director already exists for title',
            ),
        )


class TitleCountry(TitleModelMixin):
    """
    Промежуточная модель для моделей Title и Country
    """
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=('title', 'country'),
                name='Country already exists for title',
            ),
        )


class TitleActor(TitleModelMixin):
    """
    Промежуточная модель для моделей Title и Actor
    """
    actor = models.ForeignKey(
        Actor,
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=('title', 'actor'),
                name='Actor already exists for title',
            ),
        )


class TitleGenre(TitleModelMixin):
    """
    Промежуточная модель для моделей Title и Genre
    """
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=('title', 'genre'),
                name='Genre already exists for title',
            ),
        )
