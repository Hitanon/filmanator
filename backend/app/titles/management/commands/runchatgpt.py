from django.core.management.base import BaseCommand

from utils.titles import chat_gpt_evaluation


class Command(BaseCommand):
    help = 'Run ChatGPT evaluation'

    def handle(self, *args, **kwargs):
        chat_gpt_evaluation.main()
