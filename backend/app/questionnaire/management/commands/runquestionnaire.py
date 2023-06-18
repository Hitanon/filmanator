from django.core.management.base import BaseCommand

from utils.questionnaire.loader import QuestionnaireLoader
from utils.questionnaire.parser import QuestionnaireParser


class Command(BaseCommand):
    help = 'Run questionnaire parser and data loader'

    def handle(self, *args, **options):
        print('Работа начата')
        QuestionnaireParser().parse()
        QuestionnaireLoader().load()
        print('Работа закончена')
