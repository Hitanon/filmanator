from django.urls import reverse

from rest_framework.test import APIClient, APITestCase


class QuestionnaireTests(APITestCase):
    def setUp(self):
        # Urls
        self.questionnaires_url = reverse('questionnaires')

        # API client
        self.client = APIClient()

    def test_success_start_session(self):
        pass

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
