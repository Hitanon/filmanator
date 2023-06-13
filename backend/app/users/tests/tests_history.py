import json
from random import choices

from django.urls import reverse
from django.utils import timezone

from parameterized import parameterized

from rest_framework.test import APIClient, APITestCase

from rest_framework_simplejwt.tokens import AccessToken

from titles.models import Title

from users import exceptions, models, serializers


class HistoryViewTests(APITestCase):
    def setUp(self):
        # Data
        self.history_id = 1
        self.user = self._create_user()
        self._init_titles()
        self._init_history()

        # URLs
        self.histories_url = reverse('histories')
        self.history_url = lambda history_id: reverse('history', kwargs={'history_id': history_id})

        # API Client
        self.client = APIClient()

    def _create_user(self, user_data={}):
        user_data.setdefault('username', 'user')
        user_data.setdefault('email', 'user@test.com')
        user_data.setdefault('password', 'user_password')
        return models.User.objects.create(**user_data)

    def _init_titles(self):
        Title.objects.bulk_create([
            Title(
                title=f'Title {i}',
                year=2000 + i,
                imdb_rating=2.0 + i,
                votes_count=10000 * i,
                is_movie=True,
                duration=100 + 10 * i,
            ) for i in range(1, 6)
        ] + [
            Title(
                title=f'Serial {i}',
                year=2000 + i,
                imdb_rating=2.0 + i,
                votes_count=10000 * i,
                is_movie=False,
                seasons_count=i,
            ) for i in range(1, 6)
        ])

    def _init_history(self):
        history = models.History(id=self.history_id, date=timezone.now(), user=self.user)
        history.title.set(choices(Title.objects.all(), k=3))
        history.save()

    def _authorize_client(self, user):
        access_token = AccessToken.for_user(user)
        self._set_credentials(access_token)

    def _set_credentials(self, token):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def _get_exception_details(self, exc):
        return exc.default_detail

    def test_success_get_histories(self):
        self._authorize_client(self.user)

        response = self.client.get(path=self.histories_url)

        histories = models.History.objects.filter(user=self.user)
        serializer = serializers.HistorySerializer(histories, many=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), serializer.data)

    def test_failure_get_histories_is_anonymous(self):
        response = self.client.get(path=self.histories_url)

        details = self._get_exception_details(exceptions.IsAnonymous())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json.loads(response.content), details)

    def test_success_delele_history(self):
        self._authorize_client(self.user)

        response = self.client.delete(path=self.history_url(self.history_id))

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b'')
        self.assertEqual(models.History.objects.count(), 0)

    def test_failure_delete_history_is_anonymous(self):
        response = self.client.delete(path=self.history_url(self.history_id))

        details = self._get_exception_details(exceptions.IsAnonymous())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json.loads(response.content), details)
        self.assertEqual(models.History.objects.count(), 1)

    @parameterized.expand([
        ('user2', 'user2@test.com', 'user2_password'),
    ])
    def test_failure_delete_history_not_author(self, username, email, password):
        user_data = {
            'username': username,
            'email': email,
            'password': password,
        }
        user = self._create_user(user_data)
        self._authorize_client(user)

        response = self.client.delete(path=self.history_url(self.history_id))

        details = self._get_exception_details(exceptions.HistoryNotFound())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(models.History.objects.count(), 1)
        self.assertEqual(json.loads(response.content), details)

    @parameterized.expand([
        (999,),
    ])
    def test_failure_delete_history_history_not_found(self, history_id):
        self._authorize_client(self.user)

        response = self.client.delete(path=self.history_url(history_id))

        details = self._get_exception_details(exceptions.HistoryNotFound())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(models.History.objects.count(), 1)
        self.assertEqual(json.loads(response.content), details)
