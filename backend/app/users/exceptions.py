from rest_framework.exceptions import APIException

from users.mixins.exception_mixins import BaseExceptionMixin


class CustomValidationError(BaseExceptionMixin):
    status_code = 400
    default_detail = {}


class IncorrectEmailField(BaseExceptionMixin):
    status_code = 400
    default_detail = {
        'code': 'incorrect email field',
        'detail': 'Неверный email',
    }


class IncorrectUsernameField(BaseExceptionMixin):
    status_code = 400
    default_detail = {
        'code': 'incorrect username field',
        'detail': 'Неверный username',
    }


class IncorrectPasswordField(BaseExceptionMixin):
    status_code = 400
    default_detail = {
        'code': 'incorrect password field',
        'detail': 'Неверный password',
    }


class IncorrectUserData(BaseExceptionMixin):
    status_code = 400
    default_detail = {
        'code': 'incorrect user data',
        'detail': 'Неправильные данные',
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class AlreadyAuthorized(APIException):
    status_code = 401
    default_detail = {
        'detail': 'Вы уже авторизованы. Пожалуйста, сначала выйдете из аккаунта',
    }


class UserNotFound(APIException):
    status_code = 404
    default_detail = {
        'status': 'fail',
        'detail': 'Пользователь не найден',
    }
