import json

from config.settings import SESSION_LIFETIME

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from parameterized import parameterized

from questionnaire import exceptions, models, serializers

from rest_framework.test import APIClient, APITestCase

from rest_framework_simplejwt.tokens import AccessToken


class QuestionnaireTests(APITestCase):
    def setUp(self):
        # Data
        self.user = self._create_user()
        self._init_critetions()
        self._init_answers()
        self._init_questions()
        self._init_categories()

        # Urls
        self.questionnaires_url = reverse('questionnaires')
        self.questionnaire_url = lambda session_id: reverse('questionnaire', kwargs={'session_id': session_id})

        # API client
        self.client = APIClient()

    def _init_critetions(self):
        models.Criterion.objects.bulk_create([
            models.Criterion(
                id=1,
                title='Genre',
                has_limits=False,
                more=None,
                less=None,
                body='ужасы',
            ),
            models.Criterion(
                id=2,
                title='Genre',
                has_limits=False,
                more=None,
                less=None,
                body='драма',
            ),
            models.Criterion(
                id=3,
                title='Genre',
                has_limits=False,
                more=None,
                less=None,
                body='боевик',
            ),
            models.Criterion(
                id=4,
                title='Genre',
                has_limits=False,
                more=None,
                less=None,
                body='фэнтези',
            ),
            models.Criterion(
                id=5,
                title='Content Rating',
                has_limits=True,
                more=6,
                less=None,
                body='6+',
            ),
            models.Criterion(
                id=6,
                title='Content Rating',
                has_limits=True,
                more=12,
                less=None,
                body='12+',
            ),
            models.Criterion(
                id=7,
                title='Content Rating',
                has_limits=True,
                more=16,
                less=None,
                body='16+',
            ),
            models.Criterion(
                id=8,
                title='Content Rating',
                has_limits=True,
                more=18,
                less=None,
                body='18+',
            ),
        ])

    def _init_answers(self):
        answers_criterions = {
            'Ужасы': 'ужасы',
            'Ужасы': 'ужасы',
            'Ужасы': 'ужасы',
            'Ужасы': 'ужасы',
            '6+': '6+',
            '12+': '12+',
            '16+': '16+',
            '18+': '18+',
        }

        for answer_body, criterion_body in answers_criterions.items():
            answer = models.Answer.objects.create(
                body=answer_body,
                is_skip=False,
            )
            criterion = models.Criterion.objects.filter(body=criterion_body)
            answer.criterion.set(criterion)
            answer.save()

    def _init_questions(self):
        question = models.Question.objects.create(
            body='Какой жанр предпочитаете?',
        )
        question.answer.set(models.Answer.objects.filter(body='Genre'))
        question.save()

        question = models.Question.objects.create(
            body='Какой возрастной рейтинг?',
        )
        question.answer.set(models.Answer.objects.filter(body='Content Rating'))
        question.save()

    def _init_categories(self):
        category = models.Category.objects.create(
            priority=1,
            title='genre',
        )
        category.question.set(models.Question.objects.filter(body='Какой жанр предпочитаете?'))
        category.save()

        category = models.Category.objects.create(
            priority=2,
            title='content_rating',
        )
        category.question.set(models.Question.objects.filter(body='Какой возрастной рейтинг?'))
        category.save()

    def _create_user(self, user_data={}):
        user_data.setdefault('username', 'user')
        user_data.setdefault('email', 'user@test.com')
        user_data.setdefault('password', 'user_password')
        return get_user_model().objects.create(**user_data)

    def _authorize_client(self, user):
        access_token = AccessToken.for_user(user)
        self._set_credentials(access_token)

    def _set_credentials(self, token):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def _get_exception_details(self, exc):
        return exc.default_detail

    def _create_session(self, ends_at=timezone.now() + SESSION_LIFETIME):
        session = models.Session.objects.create(user=self.user, ends_at=ends_at)
        question = models.Question.objects.first()
        models.SessionState.objects.create(session=session, question=question)
        return session

    def _add_answer(self, session):
        pass

    def test_success_start_session(self):
        response = self.client.get(path=self.questionnaires_url)

        session_state = models.SessionState.objects.first()
        serializer = serializers.StartedSessionSerializer(session_state)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(models.Session.objects.count(), 1)
        self.assertEqual(models.SessionState.objects.count(), 1)
        self.assertEqual(session_state.question.category_set.first().priority, 1)
        self.assertEqual(json.loads(response.content), serializer.data)

    def test_success_get_session_state(self):
        session = self._create_session()

        response = self.client.get(path=self.questionnaire_url(session.id))

        session_state = models.SessionState.objects.get(session=session)
        serializer = serializers.SessionStateSerializer(session_state)
        self.assertEqual(response.status_code, 200, self.questionnaire_url(session.id))
        self.assertEqual(json.loads(response.content), serializer.data)

    @parameterized.expand([
        (999, ),
    ])
    def test_failure_get_session_state_incorrect_session_id(self, session_id):
        response = self.client.get(path=self.questionnaire_url(session_id))

        details = self._get_exception_details(exceptions.SessionNotFound())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.content), details)

    def test_success_auto_delete_expire_session(self):
        session = self._create_session(timezone.now() - SESSION_LIFETIME)

        response = self.client.get(path=self.questionnaire_url(session.id))

        details = self._get_exception_details(exceptions.SessionNotFound())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.content), details)
        self.assertEqual(models.Session.objects.count(), 0)
        self.assertEqual(models.SessionState.objects.count(), 0)
        self.assertEqual(models.Result.objects.count(), 0)

    def test_success_get_next_question(self):
        session = self._create_session()
        self._add_answer(session)
        data = {
            'session': session.id,
        }

        self.client.post(path=self.questionnaires_url, data=data)

    def test_failure_get_next_question_incorrect_session_id(self):
        pass

    def test_failure_get_next_question_session_id_not_found(self):
        pass

    def test_success_get_titles(self):
        pass

    def test_failure_get_titles_incorrect_session_id(self):
        pass

    def test_failure_get_titles_session_id_not_found(self):
        pass

    def test_success_delete_session(self):
        pass

    def test_failure_delete_session_incorrect_session_id(self):
        pass

    def test_failure_delete_session_session_id_not_found(self):
        pass
