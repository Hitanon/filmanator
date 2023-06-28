from django.core.management.base import BaseCommand

from utils.titles import parcing_kinopoisk


class Command(BaseCommand):
    help = 'Run kinopoisk parser'

    def handle(self, *args, **kwargs):
        parcing_kinopoisk.main()
