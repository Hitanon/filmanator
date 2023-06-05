from django.contrib import admin

from questionnaire import models


class QuestionAnswerInline(admin.TabularInline):
    model = models.QuestionAnswer
    extra = 1


@admin.register(models.Session)
class SessionAdmin(admin.ModelAdmin):
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
    inlines = (QuestionAnswerInline,)
    pass


@admin.register(models.Result)
class ResutlAdmin(admin.ModelAdmin):
    pass
