from django.contrib import admin

from titles import models


class GenreInline(admin.TabularInline):
    """
    Строка для административной панели модели Genre
    """
    model = models.Title.genre.through
    extra = 1


class DirectorInline(admin.TabularInline):
    """
    Строка для административной панели модели Director
    """
    model = models.Title.director.through
    extra = 1


class CountryInline(admin.TabularInline):
    """
    Строка для административной панели модели Country
    """
    model = models.Title.country.through
    extra = 1


class ActorInline(admin.TabularInline):
    """
    Строка для административной панели модели Actor
    """
    model = models.Title.actor.through
    extra = 1


@admin.register(models.Title)
class TitleAdmin(admin.ModelAdmin):
    """
    Административная панель произведений
    """
    inlines = (
        GenreInline,
        DirectorInline,
        CountryInline,
        ActorInline,
    )


@admin.register(models.SimilarTitle)
class SimilarTitleAdmin(admin.ModelAdmin):
    """
    Административная панель похожих произведений
    """
    pass


@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    """
    Административная панель жанров
    """
    pass


@admin.register(models.Director)
class DirectorAdmin(admin.ModelAdmin):
    """
    Административная панель жанров
    """
    pass


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    """
    Административная панель режиссеров
    """
    pass


@admin.register(models.ContentRating)
class ContentRatingAdmin(admin.ModelAdmin):
    """
    Административная панель возрастных ограничений
    """
    pass


@admin.register(models.Actor)
class ActorAdmin(admin.ModelAdmin):
    """
    Административная панель актеров
    """
    pass
