from django.db import connection

from questionnaire.models import (
    Answer,
    Category,
    Criterion,
    Question,
    Result,
    SessionState,
)


class QuestionnaireCleaner:
    models = [
        Criterion,
        Answer,
        Question,
        Category,
    ]

    linking_models = [
        SessionState,
        Result,
    ]

    @classmethod
    def clean_up_linking_tables(cls):
        for model in cls.linking_models:
            model.objects.all().delete()
            table_name = model._meta.db_table
            with connection.cursor() as cursor:
                cursor.execute(f'ALTER SEQUENCE {table_name}_id_seq RESTART WITH 1')

    @classmethod
    def clean_up(cls):
        for model in cls.models:
            model.objects.all().delete()
            table_name = model._meta.db_table
            with connection.cursor() as cursor:
                cursor.execute(f'ALTER SEQUENCE {table_name}_id_seq RESTART WITH 1')
