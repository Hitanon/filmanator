import random

from django.utils import timezone

from questionnaire import exceptions, models

from users.services import get_user


def create_session(user_id):
    user = get_user(user_id)
    return models.Session.objects.create(user=user, ends_at=timezone.now())


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
        session_state = models.SessionState.objects.get(session=session)
    except Exception as e:
        raise e
    return session_state


def check_session_id(**kwargs):
    session_id = kwargs.get('session', None)
    question_id = kwargs.get('question', None)
    answer_id = kwargs.get('answer', None)
    if not session_id:
        raise exceptions.SessionIdNotFound()
    if not question_id:
        raise exceptions.QuestionIdNotFound()
    if not answer_id:
        raise exceptions.AnswerIdNotFound()


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


def update_result(session_id, question_id, answer_id):
    session = get_session(session_id)
    question = get_question(question_id)
    answer = get_answer(answer_id)
    result = models.Result.objects.create(
        session=session,
        category=question.category_set.get(),
    )
    result.criterion.set(answer.criterion.all())


def write_result(**kwargs):
    session_id = int(kwargs['session'][0])
    question_id = int(kwargs['question'][0])
    answer_id = int(kwargs['answer'][0])
    check_answer(question_id, answer_id)
    update_result(session_id, question_id, answer_id)


def is_end(session_id):
    session = get_session(session_id)
    return models.Result.objects.filter(session=session).count() == models.Category.objects.count()


def get_next_question(session_id):
    session = get_session(session_id)
    used_categories = models.Result.objects.filter(session=session).values_list('category')
    not_used_categories = models.Category.objects.exclude(id__in=used_categories).order_by('priority')
    question = random.choice(not_used_categories[0].question.all())
    print(question)
    update_session_state(session_id, question.id)
    return question
