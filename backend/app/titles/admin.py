from django.contrib import admin

from titles import models


@admin.register(models.Actor)
class ActorAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Director)
class DirectorAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ContentRating)
class ContentRatingAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Mood)
class MoodAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ViewingMethod)
class ViewingMethodAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ViewingTime)
class ViewingTimeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.VisualAtmosphere)
class VisualAtmosphereAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Audience)
class AudienceAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Intellectuality)
class IntellectualityAdmin(admin.ModelAdmin):
    pass


@admin.register(models.NarrativeMethod)
class NarrativeMethodAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Acting)
class ActingAdmin(admin.ModelAdmin):
    pass


@admin.register(models.AmountOfDialogue)
class AmountOfDialogueAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Graphics)
class GraphicsAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Title)
class TitleAdmin(admin.ModelAdmin):
    pass


@admin.register(models.SimilarTitle)
class SimilarTitleAdmin(admin.ModelAdmin):
    pass
