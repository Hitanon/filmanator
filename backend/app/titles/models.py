from django.db import models
from django.db.models import F, Q
from django.db.models.constraints import CheckConstraint
from django.utils import timezone


class Title(models.Model):
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
    title = models.ManyToManyField(
        Title,
        related_name='titles',
    )

    similar_title = models.ManyToManyField(
        Title,
        related_name='similar_titles',
    )

    class Meta:
        constraints = (
            CheckConstraint(
                check=~Q(title=F('similar_title')),
                name='Title and similar_title is the same',
            ),
        )

    def __str__(self):
        return self.title


class Genre(models.Model):
    title = models.CharField(
        unique=True,
    )

    def __str__(self):
        return self.title


class Director(models.Model):
    name = models.CharField(
        max_length=64,
    )

    def __str__(self):
        return self.name


class Country(models.Model):
    title = models.CharField(
        max_length=64,
    )

    def __str__(self):
        return self.title


class ContentRating(models.Model):
    title = models.CharField(
        unique=True,
        max_length=8,
    )

    def __str__(self):
        return self.title


class Actor(models.Model):
    name = models.CharField(
        max_length=64,
    )

    def __str__(self):
        return self.name
