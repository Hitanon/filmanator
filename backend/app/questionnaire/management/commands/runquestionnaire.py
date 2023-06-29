from django.core.management.base import BaseCommand

from utils.questionnaire.cleaner import QuestionnaireCleaner
from utils.questionnaire.loader import QuestionnaireLoader
from utils.questionnaire.parser import QuestionnaireParser


class Command(BaseCommand):
    help = 'Run questionnaire parser and data loader' # noqa

    def add_arguments(self, parser):
        parser.add_argument('--clean-up', help='Clean? 1/0')

    def _clean_up(self, is_clean_up):
        if is_clean_up:
            self.stdout.write('Работа чистильщика началась')
            QuestionnaireCleaner.clean_up()
            self.stdout.write('Работа чистильщика закончилась')

    def _parse(self, is_cleaned_up):
        if is_cleaned_up:
            self.stdout.write('Работа парсера началась')
            QuestionnaireParser().parse()
            self.stdout.write('Работа парсера закончилась')

    def _load(self):
        self.stdout.write('Работа загрузчика началась')
        QuestionnaireLoader().load()
        self.stdout.write('Работа загрузчика закончилась')

    def handle(self, *args, **options):
        options.setdefault('clean_up', False)
        self._clean_up(options['clean_up'])
        self._parse(options['clean_up'])
        self._load()
