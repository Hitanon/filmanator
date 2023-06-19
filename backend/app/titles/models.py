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

    count_awards = models.SmallIntegerField(
        null=True,
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

    count_awards = models.SmallIntegerField(
        null=True,
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
        return str(self.value)


class AdditionalCriteria(models.Model):
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
        null=True,
    )

    mood = models.ManyToManyField(
        Mood,
        through='TitleMood',
        related_name='titles',
    )

    viewing_method = models.ManyToManyField(
        ViewingMethod,
        through='TitleViewingMethod',
        related_name='titles',
    )

    viewing_time = models.ManyToManyField(
        ViewingTime,
        through='TitleViewingTime',
        related_name='titles',
    )

    visual_atmosphere = models.ManyToManyField(
        VisualAtmosphere,
        through='TitleVisualAtmosphere',
        related_name='titles',
    )

    audience = models.ManyToManyField(
        Audience,
        through='TitleAudience',
        related_name='titles',
    )

    intellectuality = models.ManyToManyField(
        Intellectuality,
        through='TitleIntellectuality',
        related_name='titles',
    )

    narrative_method = models.ManyToManyField(
        NarrativeMethod,
        through='TitleNarrativeMethod',
        related_name='titles',
    )

    acting = models.ManyToManyField(
        Acting,
        through='TitleActing',
        related_name='titles',
    )

    amount_of_dialogue = models.ManyToManyField(
        AmountOfDialogue,
        through='TitleAmountOfDialogue',
        related_name='titles',
    )

    graphics = models.ManyToManyField(
        Graphics,
        through='TitleGraphics',
        related_name='titles',
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


class TitleMood(TitleModelMixin):
    """
    Промежуточная модель для моделей Title и Mood
    """
    mood = models.ForeignKey(
        Mood,
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=('title', 'mood'),
                name='Mood already exists for title',
            ),
        )


class TitleViewingMethod(TitleModelMixin):
    """
    Промежуточная модель для моделей Title и ViewingMethod
    """
    viewing_method = models.ForeignKey(
        ViewingMethod,
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=('title', 'viewing_method'),
                name='Viewing method already exists for title',
            ),
        )


class TitleViewingTime(TitleModelMixin):
    """
    Промежуточная модель для моделей Title и ViewingTime
    """
    viewing_time = models.ForeignKey(
        ViewingTime,
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=('title', 'viewing_time'),
                name='Viewing time already exists for title',
            ),
        )


class TitleVisualAtmosphere(TitleModelMixin):
    """
    Промежуточная модель для моделей Title и VisualAtmosphere
    """
    visual_atmosphere = models.ForeignKey(
        VisualAtmosphere,
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=('title', 'visual_atmosphere'),
                name='Visual atmosphere already exists for title',
            ),
        )


class TitleAudience(TitleModelMixin):
    """
    Промежуточная модель для моделей Title и Audience
    """
    audience = models.ForeignKey(
        Audience,
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=('title', 'audience'),
                name='Audience already exists for title',
            ),
        )


class TitleIntellectuality(TitleModelMixin):
    """
    Промежуточная модель для моделей Title и Intellectuality
    """
    intellectuality = models.ForeignKey(
        Intellectuality,
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=('title', 'intellectuality'),
                name='Intellectuality already exists for title',
            ),
        )


class TitleNarrativeMethod(TitleModelMixin):
    """
    Промежуточная модель для моделей Title и NarrativeMethod
    """
    narrative_method = models.ForeignKey(
        NarrativeMethod,
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=('title', 'narrative_method'),
                name='Narrative method already exists for title',
            ),
        )


class TitleActing(TitleModelMixin):
    """
    Промежуточная модель для моделей Title и Acting
    """
    acting = models.ForeignKey(
        Acting,
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=('title', 'acting'),
                name='Acting already exists for title',
            ),
        )


class TitleAmountOfDialogue(TitleModelMixin):
    """
    Промежуточная модель для моделей Title и AmountOfDialogue
    """
    amount_of_dialogue = models.ForeignKey(
        AmountOfDialogue,
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=('title', 'amount_of_dialogue'),
                name='AmountOfDialogue already exists for title',
            ),
        )


class TitleGraphics(TitleModelMixin):
    """
    Промежуточная модель для моделей Title и Graphics
    """
    graphics = models.ForeignKey(
        Graphics,
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=('title', 'graphics'),
                name='Graphics already exists for title',
            ),
        )
