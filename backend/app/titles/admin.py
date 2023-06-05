from django.contrib import admin

from titles import models


class GenreInline(admin.TabularInline):
    model = models.Title.genre.through
    extra = 1


class DirectorInline(admin.TabularInline):
    model = models.Title.director.through
    extra = 1


class CountryInline(admin.TabularInline):
    model = models.Title.country.through
    extra = 1


class ActorInline(admin.TabularInline):
    model = models.Title.actor.through
    extra = 1


@admin.register(models.Title)
class TitleAdmin(admin.ModelAdmin):
    inlines = (
        GenreInline,
        DirectorInline,
        CountryInline,
        ActorInline,
    )


@admin.register(models.SimilarTitle)
class SimilarTitleAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Director)
class DirectorAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ContentRating)
class ContentRatingAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Actor)
class ActorAdmin(admin.ModelAdmin):
    pass
