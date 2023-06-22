import random
from typing import Any

from config.settings import CATEGORIES_LIMIT, SESSION_LIFETIME

from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from django.utils import timezone

from questionnaire import exceptions, models, serializers
from questionnaire.utils import ResultCriterions

from titles import models as t_models
from titles.services import get_full_info_about_titles, select_titles

from users.models import History, User
from users.services import get_histories


# ----------------------------------------------------------------------------------------------------
# Create operations
# ----------------------------------------------------------------------------------------------------
def create_session(user: User | AnonymousUser) -> models.Session:
    user = user if user.is_authenticated else None
    return models.Session.objects.create(
        user=user,
        start_at=timezone.now(),
    )


def create_session_state(session: models.Session) -> models.SessionState:
    return models.SessionState.objects.create(
        session=session,
        question=select_question(session),
    )


def start_session(user: User | AnonymousUser) -> models.Session:
    session = create_session(user)
    create_session_state(session)
    return session


def write_result(session: models.Session, answer: models.Answer) -> None:
    session_state = get_session_state(session)
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


# Fix type annotation
def write_result_titles_to_history(user: User, session: models.Session, titles: Any) -> None:
    if not user.is_authenticated:
        return
    history = History.objects.create(user=user, date=session.start_at)
    history.title.set([title['id'] for title in titles])


def write_result_to_session(session: models.Session, titles: Any) -> None:
    sessions = models.Session.objects.filter(id=session.id)
    sessions.update(is_finished=True)
    for title in titles:
        models.ResultTitle.objects.create(
            session=session,
            title=t_models.Title.objects.get(id=title['id']),
            match_percentage=title['match_percentage'],
        )


# ----------------------------------------------------------------------------------------------------
# Get operations
# ----------------------------------------------------------------------------------------------------
def get_session_state(session: models.Session) -> models.SessionState:
    try:
        return models.SessionState.objects.get(session=session)
    except models.SessionState.DoesNotExist:
        raise exceptions.SessionNotFound


def get_session(session_id: int) -> models.Session:
    try:
        return models.Session.objects.get(id=session_id)
    except models.Session.DoesNotExist:
        raise exceptions.SessionNotFound()


def get_answer(answer_id: int) -> models.Answer:
    try:
        return models.Answer.objects.get(id=answer_id)
    except models.Answer.DoesNotExist:
        raise exceptions.AnswerNotFound()


def select_question(session: models.Session) -> models.Question:
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


def get_skip_answer(session_state: models.SessionState) -> models.Answer:
    category = session_state.question.category_set.first()
    temp = models.Result.objects.filter(session=session_state.session, category=category, criterion__isnull=True)
    is_skip = temp.count() or category.question.count() == 1
    return models.Answer.objects.get(is_next=True, is_skip=is_skip)


def get_skip_answered_question(session: models.Session) -> models.SkipAnsweredQuestion:
    session_state = get_session_state(session)
    skip_answer = get_skip_answer(session_state)
    return models.SkipAnsweredQuestion(session, session_state.question, skip_answer)


def get_finished_session_titles_data(session: models.Session) -> dict:
    result_titles = models.ResultTitle.objects.filter(session=session)
    serializer = serializers.ResultTitleSerializer(result_titles, many=True)
    return dict(serializer.data)


# Fix type annotation
def get_criterions(session: models.Session) -> dict:
    result_criterions = ResultCriterions()
    for result in models.Result.objects.filter(session=session, criterion__isnull=False):
        result_criterions.add_result(result)
    return result_criterions.data


def select_session_titles(session: models.Session):
    criterions = get_criterions(session)
    history = get_histories(session.user)
    return select_titles(criterions, history)


def get_titles_full_info(titles: Any) -> Any:
    return get_full_info_about_titles(titles)


# ----------------------------------------------------------------------------------------------------
# Update operations
# ----------------------------------------------------------------------------------------------------
def update_session_state(session: models.Session) -> None:
    question = select_question(session)
    session_state = get_session_state(session)
    session_state.question = question
    session_state.save()
    # return session_state


# ----------------------------------------------------------------------------------------------------
# Delete operations
# ----------------------------------------------------------------------------------------------------
def delete_session(session):
    session.delete()


# ----------------------------------------------------------------------------------------------------
# Check operations
# ----------------------------------------------------------------------------------------------------
def check_session_not_over(session: models.Session) -> None:
    if session.start_at + SESSION_LIFETIME < timezone.now():
        delete_session(session)
        raise exceptions.SessionNotFound()


def check_session_id(**kwargs):
    session_id = kwargs.get('session', None)
    if session_id is None:
        raise exceptions.SessionIdNotFound()
    session_id = int(session_id[0])
    return get_session(session_id)


def check_answer_id(**kwargs):
    answer_id = kwargs.get('answer', None)
    if answer_id is None:
        raise exceptions.AnswerIdNotFound()
    answer_id = int(answer_id[0])
    return get_answer(answer_id)


def is_end(session: models.Session) -> bool:
    results = models.Result.objects.filter(session=session)
    answered = results.filter(criterion__isnull=False).count()
    active = results.filter(Q(is_skipped=True) | Q(criterion__isnull=False)).count()
    return answered == CATEGORIES_LIMIT or active == models.Category.objects.count()


def check_is_author(session: models.Session, user: User | AnonymousUser) -> None:
    if user.is_authenticated and session.user != user:
        raise exceptions.SessionNotFound()
