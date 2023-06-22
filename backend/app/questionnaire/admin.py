from django.contrib import admin

from questionnaire import models


@admin.register(models.Session)
class SessionAdmin(admin.ModelAdmin):
    search_fields = ('session__id',)


@admin.register(models.SessionState)
class SessionStateAdmin(admin.ModelAdmin):
    search_fields = ('session__id',)


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    ordering = ('priority',)


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_filter = ('answer__criterion__title',)


@admin.register(models.Criterion)
class CriterionAdmin(admin.ModelAdmin):
    list_filter = ('title', )


@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_filter = ('criterion__title',)


@admin.register(models.Result)
class ResutlAdmin(admin.ModelAdmin):
    list_filter = ('session__id',)
    search_fields = ('session__user__username',)


@admin.register(models.ResultTitle)
class ResultTitleAdmin(admin.ModelAdmin):
    list_filter = ('session__id',)
