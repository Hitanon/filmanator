from rest_framework.test import APITestCase, APIClient

from django.urls import reverse

from questionnaire import models

from titles.models import Title


class QuestionnaireTests(APITestCase):
    def setUp(self):
        # Urls
        self.questionnaires_url = reverse('questionnaires')
        # self.questionnaire_url = reverse('questionnaire')

        # API client
        self.client = APIClient()

    def _init_criterions(self):
        Criterion = models.Criterion
        models.Criterion.objects.bulk_create([
            Criterion(title='Genre', body='Adventure'),
            Criterion(title='Genre', body='Thriller'),
            Criterion(title='Genre', body='Action'),
            Criterion(title='Genre', body='Romance'),

            Criterion(title='Content Rating', body='Romance'),
            Criterion(title='Genre', body='Romance'),
            Criterion(title='Genre', body='Romance'),
            Criterion(title='Genre', body='Romance'),
        ])

    def _init_answers(self):
        pass

    def _init_questions(self):
        pass

    def _init_categories(self):
        pass

    def _init_titles(self):
        pass

    def _init_database(self):
        self._init_criterions()
        self._init_answers()
        self._init_questions()
        self._init_categories()
        self._init_titles()

    def test_success_start_session(self):
        response = self.client.get(self.questionnaires_url)

        self.assertEqual(response.status_code, 201)

    def test_success_get_session_state(self):
        pass

    def test_failure_get_session_state_incorrect_session_id(self):
        pass

    def test_success_get_next_question(self):
        pass

    def test_failure_get_next_question_incorrect_session_id(self):
        pass

    def test_success_get_titles(self):
        pass
