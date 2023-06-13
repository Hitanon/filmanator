import json
from random import choice, sample

from django.urls import reverse

from parameterized import parameterized

from rest_framework.test import APIClient, APITestCase

from rest_framework_simplejwt.tokens import AccessToken

from titles.models import Title

from users import exceptions, models
from users.serializers import DislikedTitleSerializer


class DislikedTitleTests(APITestCase):
    def setUp(self):
        # Data
        self.title_id = None
        self.disliked_titles_count = 3
        self.user = self._create_user()
        self._init_titles()
        self._init_disliked_titles()

        # URLs
        self.disliked_titles_url = reverse('disliked_titles')
        self.disliked_title_url = lambda title_id: reverse('disliked_title', kwargs={'title_id': title_id})

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
        self.title_id = choice(Title.objects.all()).id

    def _init_disliked_titles(self):
        disliked_title = models.DislikedTitle(id=1, user=self.user)
        disliked_title.title.set(
            sample(
                list(Title.objects.all().exclude(id=self.title_id)),
                k=self.disliked_titles_count,
            ),
        )
        disliked_title.save()

    def _authorize_client(self, user):
        access_token = AccessToken.for_user(user)
        self._set_credentials(access_token)

    def _set_credentials(self, token):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def _get_exception_details(self, exc):
        return exc.default_detail

    def _add_title_to_disliked_titles(self, title_id):
        title = Title.objects.get(id=title_id)
        models.DislikedTitle.objects.get(user=self.user).title.add(title)

    def test_success_get_disliked_titles(self):
        self._authorize_client(self.user)

        response = self.client.get(path=self.disliked_titles_url)

        disliked_titles = models.DislikedTitle.objects.get(user=self.user).title.all()
        serializer = DislikedTitleSerializer(disliked_titles, many=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), serializer.data)

    def test_failure_get_disliked_titles_is_anonymous(self):
        response = self.client.get(path=self.disliked_titles_url)

        details = self._get_exception_details(exceptions.IsAnonymous())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json.loads(response.content), details)

    def test_success_add_disliked_title(self):
        self._authorize_client(self.user)
        data = {'title': self.title_id}

        response = self.client.post(path=self.disliked_titles_url, data=data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content, b'')
        self.assertEqual(
            models.DislikedTitle.objects.get(user=self.user).title.count(),
            self.disliked_titles_count + 1,
        )

    def test_failure_add_disliked_is_anonymous(self):
        data = {'title': self.title_id}

        response = self.client.post(path=self.disliked_titles_url, data=data)

        details = self._get_exception_details(exceptions.IsAnonymous())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json.loads(response.content), details)
        self.assertEqual(
            models.DislikedTitle.objects.get(user=self.user).title.count(),
            self.disliked_titles_count,
        )

    def test_failure_add_disliked_title_title_id_not_found(self):
        self._authorize_client(self.user)

        response = self.client.post(path=self.disliked_titles_url)

        details = self._get_exception_details(exceptions.TitleIdNotFound())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), details)
        self.assertEqual(
            models.DislikedTitle.objects.get(user=self.user).title.count(),
            self.disliked_titles_count,
        )

    @parameterized.expand([
        (999,),
    ])
    def test_failure_add_disliked_title_title_not_found(self, title_id):
        self._authorize_client(self.user)
        data = {'title': title_id}

        response = self.client.post(path=self.disliked_titles_url, data=data)

        details = self._get_exception_details(exceptions.TitleNotFound())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), details)
        self.assertEqual(
            models.DislikedTitle.objects.get(user=self.user).title.count(),
            self.disliked_titles_count,
        )

    def test_success_delete_disliked_title(self):
        self._authorize_client(self.user)
        self._add_title_to_disliked_titles(self.title_id)

        response = self.client.delete(path=self.disliked_title_url(self.title_id))

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b'')
        self.assertEqual(
            models.DislikedTitle.objects.get(user=self.user).title.count(),
            self.disliked_titles_count,
        )

    def test_failure_delete_disliked_title_is_anonymous(self):
        self._add_title_to_disliked_titles(self.title_id)

        response = self.client.delete(path=self.disliked_title_url(self.title_id))

        details = self._get_exception_details(exceptions.IsAnonymous())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json.loads(response.content), details)
        self.assertEqual(
            models.DislikedTitle.objects.get(user=self.user).title.count(),
            self.disliked_titles_count + 1,
        )
