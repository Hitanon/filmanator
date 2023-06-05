from django.contrib import admin

from titles import models


@admin.register(models.Title)
class TitleAdmin(admin.ModelAdmin):
    pass


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
