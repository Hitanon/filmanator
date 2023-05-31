from django.db import models


class Title(models.Model):
    id = models.CharField(primary_key=True)
    title = models.CharField(max_length=255)
    year = models.IntegerField()
    imdb_rating = models.FloatField()
    votes_count = models.IntegerField(default=0)
    is_movie = models.BooleanField()
    runtime = models.IntegerField()
    seasons_count = models.IntegerField(null=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class SimularTitle(models.Model):
    title = models.ManyToManyField(Title)
    similar_title = models.ManyToManyField(Title)


class TitleMixin(models.Model):
    """
    Миксин для классов с отношением к фильму многие-ко-многим
    """
    titles = models.ManyToManyField(Title)

    class Meta:
        abstract = True


class Actors(TitleMixin):
    id = models.CharField(primary_key=True)
    name = models.CharField(max_length=255)


class ContentRating(TitleMixin):
    title = models.CharField(max_length=255)


class Country(TitleMixin):
    title = models.CharField(max_length=255)


class Director(TitleMixin):
    id = models.CharField(primary_key=True)
    name = models.CharField(max_length=255)


class Genre(TitleMixin):
    title = models.CharField(unique=True)


class Users(models.Model):
    # поля пользователя
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.CharField(null=True)

    # связи с фильмом
    history = models.ManyToManyField(Title)
    liked_titles = models.ManyToManyField(Title)
    disliked_titles = models.ManyToManyField(Title)

    # связи с жанром
    preferred_genres = models.ManyToManyField(Genre)
    disfavored_genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.username


class Session(models.Model):
    id = models.UUIDField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    ends_at = models.DateTimeField()


class Category(models.Model):
    priority = models.IntegerField()


class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Answer(models.Model):
    body = models.CharField()
    questions = models.ManyToManyField(Question)


class Criterion(models.Model):
    title = models.CharField(unique=True)
    body = models.CharField()
    questions = models.ManyToManyField(Question)


class Result(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    criterion = models.ForeignKey(Criterion, on_delete=models.CASCADE)

