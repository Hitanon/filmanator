import json
from random import sample, choice

from django.urls import reverse

from parameterized import parameterized

from rest_framework.test import APIClient, APITestCase

from rest_framework_simplejwt.tokens import AccessToken

from titles.models import Genre

from users import exceptions, models
from users.serializers import PrefferedGenreSerializer


class PrefferedGenreTests(APITestCase):
    def setUp(self):
        # Data
        self.genre_id = None
        self.preffered_genres_count = 3
        self.user = self._create_user()
        self._init_genres()
        self._init_preffered_genres()

        # URLs
        self.preffered_genres_url = reverse('preffered_genres')
        self.preffered_genre_url = lambda genre_id: reverse('preffered_genre', kwargs={'genre_id': genre_id})

        # API Client
        self.client = APIClient()

    def _create_user(self, user_data={}):
        user_data.setdefault('username', 'user')
        user_data.setdefault('email', 'user@test.com')
        user_data.setdefault('password', 'user_password')
        return models.User.objects.create(**user_data)

    def _init_genres(self):
        Genre.objects.bulk_create([Genre(id=i, title=f'Genre {i}') for i in range(1, 10)])
        self.genre_id = choice(Genre.objects.all()).id

    def _init_preffered_genres(self):
        preffered_genre = models.PreferredGenre.objects.create(user=self.user)
        preffered_genres = sample(
            list(Genre.objects.exclude(id=self.genre_id)),
            self.preffered_genres_count,
        )
        preffered_genre.genre.set(preffered_genres)
        preffered_genre.save()

    def _authorize_client(self, user):
        access_token = AccessToken.for_user(user)
        self._set_credentials(access_token)

    def _set_credentials(self, token):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def _get_exception_details(self, exc):
        return exc.default_detail

    def _add_genre_to_preffered_genre(self, genre_id):
        genre = Genre.objects.get(id=genre_id)
        models.PreferredGenre.objects.get(user=self.user).genre.add(genre)

    def test_success_get_preffered_genres(self):
        self._authorize_client(self.user)

        response = self.client.get(path=self.preffered_genres_url)

        preffered_genres = models.PreferredGenre.objects.get(user=self.user)
        serializer = PrefferedGenreSerializer(preffered_genres.genre.all(), many=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), serializer.data)

    def test_failure_get_preffered_genres_is_anonymous(self):
        response = self.client.get(path=self.preffered_genres_url)

        details = self._get_exception_details(exceptions.IsAnonymous())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json.loads(response.content), details)

    def test_success_add_preffered_genre(self):
        self._authorize_client(self.user)
        data = {'genre': self.genre_id}

        response = self.client.post(path=self.preffered_genres_url, data=data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content, b'')
        self.assertEqual(
            models.PreferredGenre.objects.get(user=self.user).genre.count(),
            self.preffered_genres_count + 1,
        )

    def test_failure_add_preffered_genre_is_anonymous(self):
        data = {'genre': self.genre_id}

        response = self.client.post(path=self.preffered_genres_url, data=data)

        details = self._get_exception_details(exceptions.IsAnonymous())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json.loads(response.content), details)
        self.assertEqual(
            models.PreferredGenre.objects.get(user=self.user).genre.count(),
            self.preffered_genres_count,
        )

    def test_failure_add_preffered_genre_genre_id_not_found(self):
        self._authorize_client(self.user)

        response = self.client.post(path=self.preffered_genres_url)

        details = self._get_exception_details(exceptions.GenreIdNotFound())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), details)
        self.assertEqual(
            models.PreferredGenre.objects.get(user=self.user).genre.count(),
            self.preffered_genres_count,
        )

    @parameterized.expand([
        (999,),
    ])
    def test_failure_add_preffered_genre_genre_not_found(self, genre_id):
        self._authorize_client(self.user)
        data = {'genre': genre_id}

        response = self.client.post(path=self.preffered_genres_url, data=data)

        details = self._get_exception_details(exceptions.GenreNotFound())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), details)
        self.assertEqual(
            models.PreferredGenre.objects.get(user=self.user).genre.count(),
            self.preffered_genres_count,
        )

    def test_success_delete_preffered_genre(self):
        self._authorize_client(self.user)
        self._add_genre_to_preffered_genre(self.genre_id)

        response = self.client.delete(path=self.preffered_genre_url(self.genre_id))

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b'')
        self.assertEqual(
            models.PreferredGenre.objects.get(user=self.user).genre.count(),
            self.preffered_genres_count,
        )

    def test_failure_delete_preffered_genre_is_anonymous(self):
        self._add_genre_to_preffered_genre(self.genre_id)

        response = self.client.delete(path=self.preffered_genre_url(self.genre_id))

        details = self._get_exception_details(exceptions.IsAnonymous())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json.loads(response.content), details)
        self.assertEqual(
            models.PreferredGenre.objects.get(user=self.user).genre.count(),
            self.preffered_genres_count + 1,
        )
