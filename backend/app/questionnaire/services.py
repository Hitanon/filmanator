import random

from config.settings import CATEGORIES_LIMIT, SESSION_LIFETIME

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.utils import timezone

from questionnaire import exceptions, models

from titles.services import get_full_info_about_titles, select_titles

from users.models import History


# ----------------------------------------------------------------------------------------------------
# Create operations
# ----------------------------------------------------------------------------------------------------
def create_session(user: User | AnonymousUser) -> models.Session:
    user = user if user.is_authenticated else None
    ends_at = timezone.now() + SESSION_LIFETIME
    return models.Session.objects.create(user=user, ends_at=ends_at)


def get_question(session):
    used_categories = models.Result.objects.filter(
        session=session,
    ).filter(
        Q(is_skipped=True) | Q(criterion__isnull=False),
    ).values_list('category')
    not_used_categories = models.Category.objects.exclude(id__in=used_categories).order_by('-priority')
    used_questions = models.Result.objects.filter(session=session).values_list('question')
    not_used_questions = not_used_categories[0].question.exclude(id__in=used_questions)
    priorities = [question.priority for question in not_used_questions]
    question = random.choices(not_used_questions, weights=priorities, k=1)[0]
    return question


def update_session_state(session, question):
    try:
        session_state = models.SessionState.objects.get(session=session)
        session_state.question = question
        session_state.save()
    except models.SessionState.DoesNotExist:
        session_state = models.SessionState.objects.create(session=session, question=question)
    return session_state


def start_session(user: User | AnonymousUser) -> models.Session:
    session = create_session(user)
    question = get_question(session)
    session_state = update_session_state(session, question)
    return session_state


def get_skip_answer(session_state):
    category = session_state.question.category_set.first()
    temp = models.Result.objects.filter(session=session_state.session, category=category, criterion__isnull=True)
    is_skip = temp.count() or category.question.count() == 1
    return models.Answer.objects.get(is_next=True, is_skip=is_skip)


def get_skip_answered_question(session):
    session_state = get_session_state(session.id)
    skip_answer = get_skip_answer(session_state)
    return models.SkipAnsweredQuestion(session_state.session, session_state.question, skip_answer)


def check_session_not_over(session_id):
    session = get_session(session_id)
    if session.ends_at < timezone.now():
        stop_session(session.id)
        raise exceptions.SessionNotFound()


def write_result(session, answer):
    session_state = get_session_state(session.id)
    question = session_state.question
    category = question.category_set.first()
    if answer.is_skip:
        temp_results = models.Result.objects.filter(session=session, category=category)
        if temp_results:
            temp_results.update(is_skipped=True)
        else:
            temp_result = models.Result.objects.create(
                session=session,
                question=question,
                category=category,
                is_skipped=True,
            )
    else:
        temp_results = models.Result.objects.filter(session=session, category=category)
        if temp_results:
            temp_results.update(question=question)
            temp_results[0].criterion.set(answer.criterion.all())
        else:
            temp_result = models.Result.objects.create(
                session=session,
                question=question,
                category=category,
            )
            temp_result.criterion.set(answer.criterion.all())


def get_session_state(session_id):
    try:
        session = models.Session.objects.get(id=session_id)
    except models.Session.DoesNotExist:
        raise exceptions.SessionNotFound()
    session_state = models.SessionState.objects.get(session=session)
    return session_state


def get_session(session_id):
    try:
        return models.Session.objects.get(id=session_id)
    except models.Session.DoesNotExist:
        raise exceptions.SessionNotFound()


def get_answer(answer_id):
    try:
        return models.Answer.objects.get(id=answer_id)
    except models.Answer.DoesNotExist:
        raise exceptions.AnswerNotFound()


def check_answer(question_id, answer_id):
    question = get_question(question_id)
    answer = get_answer(answer_id)
    if answer not in question.answer.all():
        raise exceptions.AnswerNotInQuestionAnswers()


def check_session_id(**kwargs):
    session_id = kwargs.get('session', None)
    if session_id is None:
        raise exceptions.SessionIdNotFound()
    session_id = int(session_id[0])
    return get_session(session_id)


def check_answer_id(**kwargs):
    answer_id = kwargs.get('answer', None)
    if answer_id is None:
        raise exceptions.SessionIdNotFound()
    answer_id = int(answer_id[0])
    return get_answer(answer_id)


def check_questionnaire_post_data(**kwargs):
    return check_session_id(**kwargs), check_answer_id(**kwargs)


def is_end(session_id):
    session = get_session(session_id)
    results = models.Result.objects.filter(session=session)
    answered = results.filter(criterion__isnull=False).count()
    active = results.filter(Q(is_skipped=True) | Q(criterion__isnull=False)).count()
    return answered == CATEGORIES_LIMIT or active == models.Category.objects.count()


def stop_session(session_id):
    session = get_session(session_id)
    session.delete()


def get_criterions(session):
    result_criterions = models.ResultCriterions()
    for result in models.Result.objects.filter(session=session, criterion__isnull=False):
        result_criterions.add_result(result)
    return result_criterions.data


def get_history(session):
    user = session.user
    try:
        history = History.objects.get(user=user)
    except ObjectDoesNotExist:
        history = None
    return history


def get_titles(session_id):
    session = get_session(session_id)
    criterions = get_criterions(session)
    history = get_history(session)
    return select_titles(criterions, history)


def get_titles_full_info(titles):
    return get_full_info_about_titles(titles)


def write_result_titles_to_history(user, session_id, titles):
    if not user.is_authenticated:
        return
    session = get_session(session_id)
    history = History.objects.create(user=user, date=session.ends_at)
    history.title.set([title['id'] for title in titles])


def check_user(session, user):
    if user.is_authenticated and session.user != user:
        raise exceptions.SessionNotFound()
