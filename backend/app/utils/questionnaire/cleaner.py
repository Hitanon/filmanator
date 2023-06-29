from questionnaire.models import (
    Answer,
    Category,
    Criterion,
    Question,
)


class QuestionnaireCleaner:
    models = [
        Criterion,
        Answer,
        Question,
        Category,
    ]

    @classmethod
    def clean_up(cls):
        for model in cls.models:
            model.objects.all().delete()
