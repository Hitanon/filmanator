from django.contrib import admin

from questionnaire import models


class QuestionAnswerInline(admin.TabularInline):
    """
    Строка для административной панели промежуточной модели QuestionAnswer
    """
    model = models.QuestionAnswer
    extra = 1


@admin.register(models.Session)
class SessionAdmin(admin.ModelAdmin):
    """
    Административная панель сессий
    """
    pass


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Административная панель категорий
    """
    pass


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    """
    Административная панель вопросов
    """
    pass


@admin.register(models.Criterion)
class CriterionAdmin(admin.ModelAdmin):
    """
    Административная панель критерией
    """
    pass


@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    """
    Административная панель ответов
    """
    inlines = (QuestionAnswerInline,)


@admin.register(models.Result)
class ResutlAdmin(admin.ModelAdmin):
    """
    Административная панель результатов
    """
    pass
