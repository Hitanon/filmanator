from django.core.management.base import BaseCommand

from utils.questionnaire.cleaner import QuestionnaireCleaner
from utils.questionnaire.loader import QuestionnaireLoader
from utils.questionnaire.parser import QuestionnaireParser


class Command(BaseCommand):
    help = 'Run questionnaire parser and data loader'

    def handle(self, *args, **options):
        print('Начало работы')
        print('Работа чистильщика началась')
        QuestionnaireCleaner.clean_up()
        print('Работа чистильщика закончилась')
        print('Работа парсера началась')
        QuestionnaireParser().parse()
        print('Работа парсера закончилась')
        print('Работа загрузчика началась')
        QuestionnaireLoader().load()
        print('Работа загрузчика закончилась')
        print('Конец работы')
