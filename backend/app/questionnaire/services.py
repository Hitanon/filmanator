import random

from config.settings import SESSION_LIFETIME

from django.utils import timezone

from questionnaire import exceptions, models

from titles.services import get_full_info_about_titles, select_titles

from users.models import History
from users.services import get_user


def create_session(user_id):
    user = get_user(user_id)
    ends_at = timezone.now() + SESSION_LIFETIME
    return models.Session.objects.create(user=user, ends_at=ends_at)


def select_first_question():
    category = models.Category.objects.order_by('priority').first()
    question = random.choice(category.question.all())
    return question


def update_session_state(session_id, question_id):
    session = models.Session.objects.get(id=session_id)
    question = models.Question.objects.get(id=question_id)
    try:
        session_state = models.SessionState.objects.get(session=session)
        session_state.question = question
        session_state.save()
    except models.SessionState.DoesNotExist:
        session_state = models.SessionState.objects.create(session=session, question=question)
    return session_state


def start_session(user_id):
    session = create_session(user_id)
    question = select_first_question()
    update_session_state(session.id, question.id)
    return session


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


def get_question(question_id):
    try:
        return models.Question.objects.get(id=question_id)
    except models.Question.DoesNotExist:
        raise exceptions.QuestionNotFound()


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


def write_result(session_id, answer_id):
    session = get_session(session_id)
    session_state = get_session_state(session.id)
    answer = get_answer(answer_id)
    result = models.Result.objects.create(
        session=session,
        category=session_state.question.category_set.first(),
    )
    result.criterion.set(answer.criterion.all())


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
    return models.Result.objects.filter(session=session).count() == models.Category.objects.count()


def get_next_question(session_id):
    session = get_session(session_id)
    used_categories = models.Result.objects.filter(session=session).values_list('category')
    not_used_categories = models.Category.objects.exclude(id__in=used_categories).order_by('priority')
    question = random.choice(not_used_categories[0].question.all())
    update_session_state(session_id, question.id)
    return question


def stop_session(session_id):
    session = get_session(session_id)
    session.delete()


def get_criterions(session):
    result_criterions = models.ResultCriterions()
    for result in models.Result.objects.filter(session=session):
        result_criterions.add_result(result)
    return result_criterions.data


def get_history(session):
    user = session.user
    try:
        history = History.objects.filter(user=user)
    except:
        history = History.objects.none()
    return history


def get_titles(session_id):
    session = get_session(session_id)
    criterions = get_criterions(session)
    history = get_history(session)
    return select_titles(criterions, history)


def get_titles_full_info(titles):
    return get_full_info_about_titles(titles)


def write_result_titles_to_history(user, session_id, result_titles):
    if not user.is_authenticated:
        return
    session = get_session(session_id)
    history = History.objects.create(user=user, date=session.ends_at)
    for result_title in result_titles:
        history.title.add(*[title['id'] for title in result_title['titles']])


def check_session_not_over(session_id):
    session = get_session(session_id)
    if session.ends_at < timezone.now():
        stop_session(session.id)
        raise exceptions.SessionNotFound()
