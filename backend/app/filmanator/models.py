from django.db.models import *


class Title(Model):
    id = CharField(primary_key=True)
    title = CharField(max_length=255)
    year = IntegerField()
    imdb_rating = FloatField()
    votes_count = IntegerField(default=0)
    is_movie = BooleanField()
    runtime = IntegerField()
    seasons_count = IntegerField(null=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class SimularTitle(Model):
    title = ManyToManyField(Title)
    similar_title = ManyToManyField(Title)


class TitleMixin(Model):
    """
    Миксин для классов с отношением к фильму многие-ко-многим
    """
    titles = ManyToManyField(Title)

    class Meta:
        abstract = True


class Actors(TitleMixin):
    id = CharField(primary_key=True)
    name = CharField(max_length=255)


class ContentRating(TitleMixin):
    title = CharField(max_length=255)


class Country(TitleMixin):
    title = CharField(max_length=255)


class Director(TitleMixin):
    id = CharField(primary_key=True)
    name = CharField(max_length=255)


class Genre(TitleMixin):
    title = CharField(unique=True)


class Users(Model):
    # поля пользователя
    username = CharField(max_length=50)
    password = CharField(max_length=50)
    email = CharField(null=True)

    # связи с фильмом
    history = ManyToManyField(Title)
    liked_titles = ManyToManyField(Title)
    disliked_titles = ManyToManyField(Title)

    # связи с жанром
    preferred_genres = ManyToManyField(Genre)
    disfavored_genres = ManyToManyField(Genre)

    def __str__(self):
        return self.username


class Session(Model):
    id = UUIDField(primary_key=True)
    user = ForeignKey(Users, on_delete=CASCADE)
    ends_at = DateTimeField()


class Category(Model):
    priority = IntegerField()


class Question(Model):
    category = ForeignKey(Category, on_delete=CASCADE)


class Answer(Model):
    body = CharField()
    questions = ManyToManyField(Question)


class Criterion(Model):
    title = CharField(unique=True)
    body = CharField()
    questions = ManyToManyField(Question)


class Result(Model):
    session = ForeignKey(Session, on_delete=CASCADE)
    category = ForeignKey(Category, on_delete=CASCADE)
    criterion = ForeignKey(Criterion, on_delete=CASCADE)

