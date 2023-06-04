from django.db import models


class Title(models.Model):
    title = models.CharField(max_length=255)
    year = models.IntegerField()
    imdb_rating = models.FloatField()
    votes_count = models.IntegerField(default=0)
    is_movie = models.BooleanField()
    runtime = models.IntegerField()
    seasons_count = models.IntegerField(null=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class TitleMixin(models.Model):
    """
    Миксин для классов с отношением к фильму многие-ко-многим
    """
    titles = models.ManyToManyField(Title)

    class Meta:
        abstract = True


class SimilarTitle(models.Model):
    title = models.ManyToManyField(Title, related_name='titles')
    similar_title = models.ManyToManyField(Title, related_name='simular_titles')


class Genre(TitleMixin):
    title = models.CharField(unique=True)


class Director(TitleMixin):
    name = models.CharField(max_length=255)


class Country(TitleMixin):
    title = models.CharField(max_length=255)


class ContentRating(TitleMixin):
    value = models.IntegerField()


class Actor(TitleMixin):
    name = models.CharField(max_length=255)
