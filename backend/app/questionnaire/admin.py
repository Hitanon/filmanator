from django.contrib import admin

from questionnaire import models


@admin.register(models.Session)
class SessionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.SessionState)
class SessionStateAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Criterion)
class CriterionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Result)
class ResutlAdmin(admin.ModelAdmin):
    pass
