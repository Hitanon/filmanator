import json

from django.contrib.auth import get_user_model
from django.urls import reverse

from parameterized import parameterized

from rest_framework.test import APIClient, APITestCase

from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import AccessToken

from users import exceptions


class UserViewTests(APITestCase):
    def setUp(self):
        # Urls
        self.users_url = reverse('users')
        self.token_obtain_pair_url = reverse('token_obtain_pair')
        self.token_verify_url = reverse('token_verify')

        # Data
        self.user_model = get_user_model()

        # API client
        self.client = APIClient()

    def _get_exception_detail(self, exc):
        return exc.default_detail

    def _create_user(self, **kwargs):
        return self.user_model.objects.create_user(**kwargs)

    def _authorize_client(self, **kwargs):
        user = self._create_user(**kwargs)
        access_token = AccessToken.for_user(user)
        self._set_client_credentials(access_token)

    def _set_client_credentials(self, token):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    @parameterized.expand([
        ('user', 'user@test.com', 'user_password'),
    ])
    def test_success_create_user(self, username, email, password):
        user_data = {
            'username': username,
            'email': email,
            'password': password,
        }

        response = self.client.post(path=self.users_url, data=user_data)

        user = self.user_model.objects.get(username=username, email=email)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.user_model.objects.count(), 1)
        self.assertEqual(response.content, b'')
        self.assertIsNotNone(user)

    @parameterized.expand([
        ('user', 'error', 'user_password'),
    ])
    def test_failure_create_user_incorrect_email(self, username, email, password):
        user_data = {
            'username': username,
            'email': email,
            'password': password,
        }

        response = self.client.post(path=self.users_url, data=user_data)

        details = self._get_exception_detail(exceptions.IncorrectEmailField())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.user_model.objects.count(), 0)
        self.assertEqual(json.loads(response.content), details)

    @parameterized.expand([
        ('error!', 'user@test.com', 'user_password'),
        ('error@', 'user@test.com', 'user_password'),
        ('error#', 'user@test.com', 'user_password'),
        ('error$', 'user@test.com', 'user_password'),
        ('error%', 'user@test.com', 'user_password'),
        ('error^', 'user@test.com', 'user_password'),
        ('error(', 'user@test.com', 'user_password'),
        ('error)', 'user@test.com', 'user_password'),
        ('error-', 'user@test.com', 'user_password'),
        ('error=', 'user@test.com', 'user_password'),
        ('error/', 'user@test.com', 'user_password'),
        ('error\\', 'user@test.com', 'user_password'),
        ('error,', 'user@test.com', 'user_password'),
        ('error.', 'user@test.com', 'user_password'),
        ('error`', 'user@test.com', 'user_password'),
        ('error~', 'user@test.com', 'user_password'),
        ('error+', 'user@test.com', 'user_password'),
        ("error\'", 'user@test.com', 'user_password'),
    ])
    def test_failure_create_user_incorrect_username(self, username, email, password):
        user_data = {
            'username': username,
            'email': email,
            'password': password,
        }

        response = self.client.post(path=self.users_url, data=user_data)

        details = self._get_exception_detail(exceptions.IncorrectUsernameField())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.user_model.objects.count(), 0)
        self.assertEqual(json.loads(response.content), details)

    @parameterized.expand([
        ('user', 'user@test.com', ''),
    ])
    def test_failure_create_user_incorrect_password(self, username, email, password):
        user_data = {
            'username': username,
            'email': email,
            'password': password,
        }

        response = self.client.post(path=self.users_url, data=user_data)

        details = self._get_exception_detail(exceptions.IncorrectPasswordField())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.user_model.objects.count(), 0)
        self.assertEqual(json.loads(response.content), details)

    @parameterized.expand([
        ('user', 'user@test.com', 'user_password'),
    ])
    def test_failure_create_user_email_and_username_exists(self, username, email, password):
        user_data = {
            'username': username,
            'email': email,
            'password': password,
        }
        self._create_user(**user_data)

        response = self.client.post(path=self.users_url, data=user_data)

        details = {
            'username': self._get_exception_detail(exceptions.IncorrectUsernameField(code='unique')),
            'email': self._get_exception_detail(exceptions.IncorrectEmailField(code='unique')),
        }
        response_content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.user_model.objects.count(), 1)
        self.assertEqual(response_content, details)

    @parameterized.expand([
        ('user', 'user@test.com', 'user_password', 'user2'),
    ])
    def test_failure_create_user_email_exists(self, username, email, password, username2):
        user_data = {
            'username': username,
            'email': email,
            'password': password,
        }
        self._create_user(**user_data)
        user_data['username'] = username2

        response = self.client.post(path=self.users_url, data=user_data)

        details = self._get_exception_detail(exceptions.IncorrectEmailField(code='unique'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.user_model.objects.count(), 1)
        self.assertEqual(json.loads(response.content), details)

    @parameterized.expand([
        ('user', 'user@test.com', 'user_password', 'user2@test.com'),
    ])
    def test_failure_create_user_username_exists(self, username, email, password, email2):
        user_data = {
            'username': username,
            'email': email,
            'password': password,
        }
        self._create_user(**user_data)
        user_data['email'] = email2

        response = self.client.post(path=self.users_url, data=user_data)

        details = self._get_exception_detail(exceptions.IncorrectUsernameField(code='unique'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.user_model.objects.count(), 1)
        self.assertEqual(json.loads(response.content), details)

    @parameterized.expand([
        (
            {
                'username': 'user',
                'email': 'user@test.com',
                'password': 'user_password',
            },
            {
                'username': 'user2',
                'email': 'user2@test.com',
                'password': 'user2_password',
            },
        ),
    ])
    def test_failure_create_user_is_authorized(self, user_data_1, user_data_2):
        self._authorize_client(**user_data_1)

        response = self.client.post(path=self.users_url, data=user_data_2)

        details = self._get_exception_detail(exceptions.AlreadyAuthorized())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(self.user_model.objects.count(), 1)
        self.assertEqual(json.loads(response.content), details)

    @parameterized.expand([
        ('user', 'user@test.com', 'user_password'),
    ])
    def test_success_authorization(self, username, email, password):
        user_data = {
            'username': username,
            'email': email,
            'password': password,
        }
        self._create_user(**user_data)
        del user_data['username']

        response = self.client.post(path=self.token_obtain_pair_url, data=user_data)

        response_content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response_content.get('access', None))
        self.assertIsNotNone(response_content.get('refresh', None))

    @parameterized.expand([
        ('user', 'user@test.com', 'user_password'),
    ])
    def test_failure_authorization_miss_email(self, username, email, password):
        user_data = {
            'username': username,
            'email': email,
            'password': password,
        }
        self._create_user(**user_data)
        del user_data['email']

        response = self.client.post(path=self.token_obtain_pair_url, data=user_data)

        detailts = self._get_exception_detail(exceptions.IncorrectEmailField())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), detailts)

    @parameterized.expand([
        ('user', 'user@test.com', 'user_password'),
    ])
    def test_failure_authorization_miss_password(self, username, email, password):
        user_data = {
            'username': username,
            'email': email,
            'password': password,
        }
        self._create_user(**user_data)
        del user_data['password']

        response = self.client.post(path=self.token_obtain_pair_url, data=user_data)

        detailts = self._get_exception_detail(exceptions.IncorrectPasswordField())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), detailts)

    @parameterized.expand([
        ('123.123.123',),
    ])
    def test_failure_authorization_wrong_token(self, invalid_access_token):
        data = {
            'token': invalid_access_token,
        }

        response = self.client.post(path=self.token_verify_url, data=data)

        exc = InvalidToken(detail='Токен недействителен или просрочен', code='token_not_valid')
        details = {
            'detail': exc.default_detail,
            'code': exc.get_codes()['code'],
        }
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json.loads(response.content), details)

    @parameterized.expand([
        ('user', 'user@test.com', 'user_password'),
    ])
    def test_success_delete_user(self, username, email, password):
        user_data = {
            'username': username,
            'email': email,
            'password': password,
        }
        self._authorize_client(**user_data)

        response = self.client.delete(path=self.users_url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b'')
        self.assertEqual(self.user_model.objects.count(), 0)

    @parameterized.expand([
        ('user', 'user@test.com', 'user_password'),
    ])
    def test_failure_delete_user_is_anonymous(self, username, email, password):
        user_data = {
            'username': username,
            'email': email,
            'password': password,
        }
        self._create_user(**user_data)

        response = self.client.delete(path=self.users_url)

        details = self._get_exception_detail(exceptions.IsAnonymous())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json.loads(response.content), details)
        self.assertEqual(self.user_model.objects.count(), 1)
