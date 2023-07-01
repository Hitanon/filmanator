from celery import shared_task

from django.conf import settings
from django.utils import timezone

from questionnaire.models import Session


@shared_task
def delete_expire_sessions():
    current_date = timezone.now() - settings.SESSION_LIFETIME
    Session.objects.filter(start_at__lte=current_date).delete()
